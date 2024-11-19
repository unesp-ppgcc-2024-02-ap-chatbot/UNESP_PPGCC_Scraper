import { Chat } from "@/components/chat";
import { generateUUID } from "@/lib/utils";
import { auth } from "@/app/(auth)/auth";
import { redirect } from "next/navigation";

export default async function Page() {
    const session = await auth();
    if (!session || !session.user) {
        redirect("/login");
    }

    const id = generateUUID();
    return <Chat key={id} id={id} initialMessages={[]} isCompare={false} />;
}
