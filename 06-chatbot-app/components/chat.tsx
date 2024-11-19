"use client";

import type { Attachment, Message } from "ai";
import { useChat } from "ai/react";
import { AnimatePresence } from "framer-motion";
import { useState } from "react";
import useSWR, { useSWRConfig } from "swr";
import { useWindowSize } from "usehooks-ts";

import { ChatHeader } from "@/components/chat-header";
import { PreviewMessage, ThinkingMessage } from "@/components/message";
import { useScrollToBottom } from "@/components/use-scroll-to-bottom";
import type { Vote } from "@/lib/db/schema";
import { fetcher } from "@/lib/utils";

import { Block, type UIBlock } from "./block";
import { BlockStreamHandler } from "./block-stream-handler";
import { MultimodalInput } from "./multimodal-input";
import { Overview } from "./overview";
import { DEFAULT_MODEL_NAME, models, ModelIds } from "@/lib/ai/models";
import { ALLOWED_SEARCH_METHODS } from "@/lib/ai/search-options";

export interface ChatOptions {
    modelId: ModelIds;
    searchType: ALLOWED_SEARCH_METHODS;
}

export function Chat({
    id,
    initialMessages,
    isCompare = false,
}: {
    id: string;
    initialMessages: Array<Message>;
    isCompare?: boolean;
}) {
    const { mutate } = useSWRConfig();
    const [chatOptions, setChatOptions] = useState<ChatOptions>({
        modelId: DEFAULT_MODEL_NAME,
        searchType: "hybrid",
    });

    const {
        messages,
        setMessages,
        handleSubmit,
        input,
        setInput,
        append,
        isLoading,
        stop,
        data: streamingData,
    } = useChat({
        body: {
            id,
            modelId: chatOptions.modelId,
            searchType: chatOptions.searchType,
            isCompare: isCompare,
        },
        initialMessages,
        onFinish: () => {
            mutate("/api/history");
        },
    });

    const { width: windowWidth = 1920, height: windowHeight = 1080 } =
        useWindowSize();

    const [block, setBlock] = useState<UIBlock>({
        documentId: "init",
        content: "",
        title: "",
        status: "idle",
        isVisible: false,
        boundingBox: {
            top: windowHeight / 4,
            left: windowWidth / 4,
            width: 250,
            height: 50,
        },
    });

    const { data: votes } = useSWR<Array<Vote>>(
        `/api/vote?chatId=${id}`,
        fetcher
    );

    const [messagesContainerRef, messagesEndRef] =
        useScrollToBottom<HTMLDivElement>();

    const [attachments, setAttachments] = useState<Array<Attachment>>([]);

    return (
        <>
            <div className="flex flex-col min-w-0 h-dvh bg-background">
                <ChatHeader
                    chatOptions={chatOptions}
                    isCompare={isCompare}
                    setChatOptions={setChatOptions}
                />
                <div
                    ref={messagesContainerRef}
                    className="flex flex-col min-w-0 gap-6 flex-1 overflow-y-scroll pt-4"
                >
                    {messages.length === 0 && <Overview />}

                    {messages.map((message, index) => (
                        <PreviewMessage
                            key={message.id}
                            chatId={id}
                            message={message}
                            block={block}
                            setBlock={setBlock}
                            isLoading={
                                isLoading && messages.length - 1 === index
                            }
                            vote={
                                votes
                                    ? votes.find(
                                          (vote) =>
                                              vote.messageId === message.id
                                      )
                                    : undefined
                            }
                            isCompare={isCompare}
                            chatOptions={chatOptions}
                        />
                    ))}

                    {isLoading &&
                        messages.length > 0 &&
                        messages[messages.length - 1].role === "user" && (
                            <ThinkingMessage />
                        )}

                    <div
                        ref={messagesEndRef}
                        className="shrink-0 min-w-[24px] min-h-[24px]"
                    />
                </div>
                <form className="flex mx-auto px-4 bg-background pb-4 md:pb-6 gap-2 w-full md:max-w-3xl">
                    <MultimodalInput
                        chatId={id}
                        input={input}
                        setInput={setInput}
                        handleSubmit={handleSubmit}
                        isLoading={isLoading}
                        stop={stop}
                        attachments={attachments}
                        setAttachments={setAttachments}
                        messages={messages}
                        setMessages={setMessages}
                        append={append}
                        isCompare={isCompare}
                    />
                </form>
            </div>

            <AnimatePresence>
                {block?.isVisible && (
                    <Block
                        chatId={id}
                        input={input}
                        setInput={setInput}
                        handleSubmit={handleSubmit}
                        isLoading={isLoading}
                        stop={stop}
                        attachments={attachments}
                        setAttachments={setAttachments}
                        append={append}
                        block={block}
                        setBlock={setBlock}
                        messages={messages}
                        setMessages={setMessages}
                        votes={votes}
                        chatOptions={chatOptions}
                        isCompare={isCompare}
                    />
                )}
            </AnimatePresence>

            <BlockStreamHandler
                streamingData={streamingData}
                setBlock={setBlock}
            />
        </>
    );
}
