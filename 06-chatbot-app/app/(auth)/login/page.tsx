"use client";

import { Button } from "@/components/ui/button";
import { signIn } from "next-auth/react";

export default function Page() {
    return (
        <div className="flex h-dvh w-screen items-start pt-12 md:pt-0 md:items-center justify-center bg-background">
            <div className="w-full max-w-md overflow-hidden rounded-2xl flex flex-col gap-12">
                <div className="flex flex-col items-center justify-center gap-2 px-4 text-center sm:px-16">
                    <h3 className="text-xl font-semibold dark:text-zinc-50">
                        Faça login com sua conta UNESP
                    </h3>
                </div>
                <Button
                    onClick={() =>
                        signIn("google", {
                            redirectTo: "/",
                        })
                    }
                >
                    Login com o Google
                </Button>
                <div className="rounded-md bg-yellow-50 p-4">
                    <div className="flex">
                        <div className="flex-shrink-0">
                            <svg
                                className="h-5 w-5 text-yellow-400"
                                viewBox="0 0 20 20"
                                fill="currentColor"
                            >
                                <path
                                    fillRule="evenodd"
                                    d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                                    clipRule="evenodd"
                                />
                            </svg>
                        </div>
                        <div className="ml-3">
                            <h3 className="text-sm font-medium text-yellow-800">
                                Atenção
                            </h3>
                            <div className="mt-2 text-sm text-yellow-700">
                                <p>
                                    Apenas e-mails com domínio @unesp.br são
                                    permitidos.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
