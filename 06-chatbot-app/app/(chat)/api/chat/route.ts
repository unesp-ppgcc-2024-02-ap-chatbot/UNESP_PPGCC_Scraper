import {
    type Message,
    StreamData,
    convertToCoreMessages,
    streamObject,
    streamText,
} from "ai";
import { z } from "zod";
const apiServer = process.env.API_SEARCH_SERVER;

import { auth } from "@/app/(auth)/auth";
import { customModel } from "@/lib/ai";
import { ModelIds, models } from "@/lib/ai/models";
import { systemPrompt } from "@/lib/ai/prompts";
import {
    deleteChatById,
    getChatById,
    getDocumentById,
    saveChat,
    saveDocument,
    saveMessages,
    saveSuggestions,
} from "@/lib/db/queries";
import type { Suggestion } from "@/lib/db/schema";
import {
    generateUUID,
    getMostRecentUserMessage,
    sanitizeResponseMessages,
} from "@/lib/utils";

import { generateTitleFromUserMessage } from "../../actions";
import { ALLOWED_SEARCH_METHODS } from "@/lib/ai/search-options";

export const maxDuration = 60;

type AllowedTools =
    | "createDocument"
    | "updateDocument"
    | "requestSuggestions"
    | "getWeather";

const blocksTools: AllowedTools[] = [];

const weatherTools: AllowedTools[] = [];

const allTools: AllowedTools[] = [...blocksTools, ...weatherTools];

export async function POST(request: Request) {
    const {
        id,
        messages,
        modelId,
        searchType,
        isCompare,
    }: {
        id: string;
        messages: Array<Message>;
        modelId: ModelIds;
        searchType: ALLOWED_SEARCH_METHODS;
        isCompare?: boolean;
    } = await request.json();

    console.log("MODEL ID", modelId);
    console.log("SEARCH TYPE", searchType);

    const lastUserMessage = messages[messages.length - 1];
    const contentLastUserMessage = lastUserMessage.content;
    const searchUrlPart =
        searchType === "hybrid" ? "search_hybrid_rerank" : "search_semantic";
    const apiResult = await fetch(
        `${apiServer}/api/${searchUrlPart}?q=${contentLastUserMessage}&result_limit=5`
    );
    const apiResultData = await apiResult.json();
    const results =
        searchType === "hybrid"
            ? apiResultData.result.points
            : apiResultData.result;
    const topResultsContent = (results || [])
        .map(
            (result: any, index: number) =>
                `Result: ${index + 1} \n${
                    searchType === "hybrid"
                        ? result.payload.content
                        : result.content
                }\n\n`
        )
        .reverse()
        .join(" ");
    console.log("topResultsContent", topResultsContent);

    const prompt = `
        ----Start of user question----
        ${lastUserMessage.content}
        ----End of user question----
        ----Start of context----
        ${topResultsContent}
        ----End of context----
        `;

    // update the prompt with the user message
    // messages[messages.length - 1].content = prompt;

    const session = await auth();

    if (!session || !session.user || !session.user.id) {
        return new Response("Unauthorized", { status: 401 });
    }

    const model = models.find((model) => model.id === modelId);

    if (!model) {
        return new Response("Model not found", { status: 404 });
    }
    // console.log("messages", JSON.stringify(messages, null, 2));

    const coreMessages = convertToCoreMessages(messages);
    const userMessage = getMostRecentUserMessage(coreMessages);

    if (!userMessage) {
        return new Response("No user message found", { status: 400 });
    }

    const chat = await getChatById({ id });

    if (!chat) {
        console.log("session before save", JSON.stringify(session, null, 2));
        const title = await generateTitleFromUserMessage({
            message: userMessage,
        });
        await saveChat({ id, userId: session.user.id, title });
    }

    await saveMessages({
        messages: [
            {
                ...userMessage,
                id: generateUUID(),
                createdAt: new Date(),
                chatId: id,
            },
        ],
    });

    const streamingData = new StreamData();
    const copyCoreMessages = JSON.parse(JSON.stringify(coreMessages));
    copyCoreMessages[copyCoreMessages.length - 1].content = prompt;
    // console.log("copyCoreMessages", JSON.stringify(copyCoreMessages, null, 2));

    const result = await streamText({
        model: customModel(model.apiIdentifier),
        system: systemPrompt,
        messages: copyCoreMessages,
        maxSteps: 5,
        onFinish: async ({ responseMessages }) => {
            if (session.user?.id) {
                try {
                    const responseMessagesWithoutIncompleteToolCalls =
                        sanitizeResponseMessages(responseMessages);

                    await saveMessages({
                        messages:
                            responseMessagesWithoutIncompleteToolCalls.map(
                                (message) => {
                                    const messageId = generateUUID();

                                    if (message.role === "assistant") {
                                        streamingData.appendMessageAnnotation({
                                            messageIdFromServer: messageId,
                                            modelId: modelId,
                                            searchType: searchType,
                                        });
                                    }

                                    return {
                                        id: messageId,
                                        chatId: id,
                                        role: message.role,
                                        content: message.content,
                                        createdAt: new Date(),
                                    };
                                }
                            ),
                    });
                } catch (error) {
                    console.error("Failed to save chat");
                }
            }

            streamingData.close();
        },
        experimental_telemetry: {
            isEnabled: true,
            functionId: "stream-text",
        },
    });

    return result.toDataStreamResponse({
        data: streamingData,
    });
}

export async function DELETE(request: Request) {
    const { searchParams } = new URL(request.url);
    const id = searchParams.get("id");

    if (!id) {
        return new Response("Not Found", { status: 404 });
    }

    const session = await auth();

    if (!session || !session.user) {
        return new Response("Unauthorized", { status: 401 });
    }

    try {
        const chat = await getChatById({ id });

        if (chat.userId !== session.user.id) {
            return new Response("Unauthorized", { status: 401 });
        }

        await deleteChatById({ id });

        return new Response("Chat deleted", { status: 200 });
    } catch (error) {
        return new Response("An error occurred while processing your request", {
            status: 500,
        });
    }
}
