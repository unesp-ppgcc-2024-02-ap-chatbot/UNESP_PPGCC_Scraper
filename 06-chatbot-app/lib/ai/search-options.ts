export type ALLOWED_SEARCH_METHODS = "semantic" | "hybrid";

export const SEARCH_METHODS: Record<ALLOWED_SEARCH_METHODS, string> = {
    semantic: "Semantic (bge-m3)",
    hybrid: "Hybrid Fusion RRF (bge-m3 + bm25)",
};

export const SEARCH_METHODS_LIST: {
    id: ALLOWED_SEARCH_METHODS;
    label: string;
}[] = Object.entries(SEARCH_METHODS).map(([id, value]) => ({
    id: id as ALLOWED_SEARCH_METHODS,
    label: value,
}));
