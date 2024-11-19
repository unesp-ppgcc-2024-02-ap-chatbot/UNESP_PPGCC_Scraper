import { redirect } from "next/navigation";
import { auth } from "@/app/(auth)/auth";
import { generateUUID } from "@/lib/utils";
import { Chat } from "@/components/chat";

export default async function Page() {
    const session = await auth();

    if (!session || !session.user) {
        redirect("/login");
    }
    const id1 = generateUUID();
    const id2 = generateUUID();

    return (
        <div className="flex flex-col md:flex-row w-full gap-4">
            <div className="flex-1">
                <Chat
                    key={id1}
                    id={id1}
                    initialMessages={[]}
                    isCompare={true}
                />
            </div>
            <div className="flex-1">
                <Chat
                    key={id2}
                    id={id2}
                    initialMessages={[]}
                    isCompare={true}
                />
            </div>
        </div>
    );
}
