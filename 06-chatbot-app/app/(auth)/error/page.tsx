"use client";

import { Button } from "@/components/ui/button";
import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";

export default function Page() {
    const router = useRouter();
    return (
        <div className="flex h-dvh w-screen items-start pt-12 md:pt-0 md:items-center justify-center bg-background">
            <div className="w-full max-w-md overflow-hidden rounded-2xl flex flex-col gap-12">
                <div className="rounded-md bg-yellow-50 p-4">
                    <div className="flex">
                        <div className="ml-3">
                            <h3 className="text-sm font-medium text-red-800">
                                Atenção
                            </h3>
                            <div className="mt-2 text-sm text-red-700">
                                <p>
                                    Apenas e-mails com domínio @unesp.br são
                                    permitidos.
                                </p>
                                <Button
                                    className="mt-4"
                                    onClick={() => router.push("/login")}
                                >
                                    Ir para o login
                                </Button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
