"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useWindowSize } from "usehooks-ts";

import { ModelSelector } from "@/components/model-selector";
import { SidebarToggle } from "@/components/sidebar-toggle";
import { Button } from "@/components/ui/button";
import { BetterTooltip } from "@/components/ui/tooltip";
import { PlusIcon, VercelIcon } from "./icons";
import { useSidebar } from "./ui/sidebar";
import Image from "next/image";
import { DEFAULT_MODEL_NAME, ModelIds, models } from "@/lib/ai/models";
import { Dispatch, SetStateAction } from "react";
import { ChatOptions } from "./chat";
import { SearchSelector } from "./search-selector";

export function ChatHeader({
    chatOptions,
    isCompare,
    setChatOptions,
}: {
    chatOptions: ChatOptions;
    setChatOptions: Dispatch<SetStateAction<ChatOptions>>;
    isCompare: boolean;
}) {
    const router = useRouter();
    const { open } = useSidebar();
    const defaultModel = models.find(
        (model) => model.id === DEFAULT_MODEL_NAME
    );

    const { width: windowWidth } = useWindowSize();

    return (
        <header className="flex sticky top-0 bg-background py-1.5 items-center px-2 md:px-2 gap-2">
            {!isCompare && <SidebarToggle />}
            {(!open || windowWidth < 768) && (
                <BetterTooltip content="New Chat">
                    <Button
                        variant="outline"
                        className="order-2 md:order-1 md:px-2 px-2 md:h-fit ml-auto md:ml-0"
                        onClick={() => {
                            router.push("/");
                            router.refresh();
                        }}
                    >
                        <PlusIcon />
                        <span className="md:sr-only">New Chat</span>
                    </Button>
                </BetterTooltip>
            )}
            {isCompare ? (
                <>
                    <ModelSelector
                        selectedModelId={chatOptions.modelId}
                        className="order-1 md:order-2"
                        setChatOptions={setChatOptions}
                    />
                    <SearchSelector
                        searchId={chatOptions.searchType}
                        setChatOptions={setChatOptions}
                        className="order-3"
                    />
                </>
            ) : (
                <span className="text-sm">{defaultModel?.label}</span>
            )}
            <Image
                className="hidden md:flex py-1.5 px-2 h-fit order-4 md:ml-auto"
                src="/images/unesp.svg"
                alt="Logo"
                width={137}
                height={55}
            />
        </header>
    );
}
