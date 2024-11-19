import { createOpenAI, openai } from "@ai-sdk/openai";
import { experimental_wrapLanguageModel as wrapLanguageModel } from "ai";

import { customMiddleware } from "./custom-middleware";

export const customModel = (apiIdentifier: string) => {
    if (apiIdentifier.includes("fireworks")) {
        const fireworks = createOpenAI({
            apiKey: process.env.FIREWORKS_API_KEY ?? "",
            baseURL: "https://api.fireworks.ai/inference/v1",
        });
        return fireworks(apiIdentifier);
    } else {
        return wrapLanguageModel({
            model: openai(apiIdentifier),
            middleware: customMiddleware,
            providerId: "",
        });
    }
};
