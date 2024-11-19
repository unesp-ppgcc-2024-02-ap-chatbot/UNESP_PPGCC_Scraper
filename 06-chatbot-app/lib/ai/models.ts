// Define your models here.
export type ModelIds = "gpt-4o-mini" | "llama-3.2-11b";
export interface Model {
    id: ModelIds;
    label: string;
    apiIdentifier: string;
    description: string;
}

export const models: Array<Model> = [
    {
        id: "gpt-4o-mini",
        label: "GPT 4o mini",
        apiIdentifier: "gpt-4o-mini",
        description: "Small model for fast, lightweight tasks",
    },
    {
        id: "llama-3.2-11b",
        label: "Llama 3.2 11B",
        apiIdentifier:
            "accounts/fireworks/models/llama-v3p2-11b-vision-instruct",
        description: "Open source model",
    },
] as const;

export const DEFAULT_MODEL_NAME: ModelIds = "gpt-4o-mini";
