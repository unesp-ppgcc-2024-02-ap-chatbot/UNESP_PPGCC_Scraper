import { authConfig } from "./auth.config";
import NextAuth, { type User, type Session } from "next-auth";

export const {
    handlers: { GET, POST },
    auth,
    signIn,
    signOut,
} = NextAuth({
    ...authConfig,
    session: {
        strategy: "jwt",
    },
});
