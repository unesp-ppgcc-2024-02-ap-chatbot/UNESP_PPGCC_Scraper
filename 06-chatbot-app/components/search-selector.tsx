"use client";

import {
    Dispatch,
    SetStateAction,
    startTransition,
    useMemo,
    useOptimistic,
    useState,
} from "react";

import { saveModelId } from "@/app/(chat)/actions";
import { Button } from "@/components/ui/button";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { DEFAULT_MODEL_NAME, ModelIds, models } from "@/lib/ai/models";
import { cn } from "@/lib/utils";

import { CheckCirclFillIcon, ChevronDownIcon } from "./icons";
import { ChatOptions } from "./chat";
import {
    ALLOWED_SEARCH_METHODS,
    SEARCH_METHODS_LIST,
} from "@/lib/ai/search-options";

export function SearchSelector({
    searchId,
    setChatOptions,
    className,
}: {
    searchId: ALLOWED_SEARCH_METHODS;
    setChatOptions: Dispatch<SetStateAction<ChatOptions>>;
} & React.ComponentProps<typeof Button>) {
    const [open, setOpen] = useState(false);
    const [optimisticSearchId, setOptimisticModelId] = useOptimistic(searchId);

    const selectedSearch = useMemo(
        () =>
            SEARCH_METHODS_LIST.find((data) => data.id === optimisticSearchId),
        [optimisticSearchId]
    );

    return (
        <DropdownMenu open={open} onOpenChange={setOpen}>
            <DropdownMenuTrigger
                asChild
                className={cn(
                    "w-fit data-[state=open]:bg-accent data-[state=open]:text-accent-foreground",
                    className
                )}
            >
                <Button variant="outline" className="md:px-2 md:h-[34px]">
                    {selectedSearch?.label}
                    <ChevronDownIcon />
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="start" className="min-w-[300px]">
                {SEARCH_METHODS_LIST.map((item) => (
                    <DropdownMenuItem
                        key={item.id}
                        onSelect={() => {
                            setOpen(false);

                            startTransition(() => {
                                setOptimisticModelId(item.id);
                                setChatOptions((prev) => ({
                                    ...prev,
                                    searchType: item.id,
                                }));
                            });
                        }}
                        className="gap-4 group/item flex flex-row justify-between items-center"
                        data-active={item.id === optimisticSearchId}
                    >
                        <div className="flex flex-col gap-1 items-start">
                            {item.label}
                        </div>
                        <div className="text-primary dark:text-primary-foreground opacity-0 group-data-[active=true]/item:opacity-100">
                            <CheckCirclFillIcon />
                        </div>
                    </DropdownMenuItem>
                ))}
            </DropdownMenuContent>
        </DropdownMenu>
    );
}
