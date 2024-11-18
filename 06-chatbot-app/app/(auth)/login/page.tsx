'use client';

import { Button } from "@/components/ui/button";
import { signIn } from "next-auth/react"

export default function Page() {
  return (
    <div className="flex h-dvh w-screen items-start pt-12 md:pt-0 md:items-center justify-center bg-background">
      <div className="w-full max-w-md overflow-hidden rounded-2xl flex flex-col gap-12">
        <div className="flex flex-col items-center justify-center gap-2 px-4 text-center sm:px-16">
          <h3 className="text-xl font-semibold dark:text-zinc-50">Sign In</h3>
        </div>
        <Button onClick={() => signIn("google")}>Signin</Button>
      </div>
    </div>
  );
}
