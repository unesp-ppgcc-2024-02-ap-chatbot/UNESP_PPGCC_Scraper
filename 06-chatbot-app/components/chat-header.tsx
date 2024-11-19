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
            <Link
                href="https://github.com/unesp-ppgcc-2024-02-ap-chatbot/unesp-ppgcc-chatbot"
                target="_blank"
                className="order-3 md:order-4"
            >
                <Button variant="ghost" size="icon">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    >
                        <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22" />
                    </svg>
                </Button>
            </Link>
            {!isCompare && (
                <Link href="/about" className="ml-auto">
                    <Button
                        variant="ghost"
                        className="order-3 md:order-4 text-sm md:text-base text-blue-500 hover:underline"
                    >
                        Sobre o projeto
                    </Button>
                </Link>
            )}
            <Image
                className="hidden md:flex py-1.5 px-2 h-fit order-4"
                src="/images/unesp.svg"
                alt="Logo"
                width={137}
                height={55}
            />
        </header>
    );
}
