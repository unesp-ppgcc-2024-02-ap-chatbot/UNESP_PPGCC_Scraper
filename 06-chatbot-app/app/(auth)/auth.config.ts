import { createUser, getUser, getUserById } from "@/lib/db/queries";
import type { NextAuthConfig } from "next-auth";
import Google from "next-auth/providers/google";
import NextAuth, { type User, type Session } from "next-auth";

interface ExtendedSession extends Session {
    user: User;
}

export const authConfig = {
    pages: {
        signIn: "/login",
        newUser: "/",
        error: "/error",
    },
    providers: [Google],
    callbacks: {
        async authorized(allData) {
            const {
                auth,
                request: { nextUrl },
            } = allData;
            if (auth) {
                const isLoggedIn = !!auth?.user;
                const isOnChat = nextUrl.pathname.startsWith("/");
                const isOnRegister = nextUrl.pathname.startsWith("/register");
                const isOnLogin = nextUrl.pathname.startsWith("/login");
                const email = auth?.user?.email;
                const domain = email?.split("@")[1].toLowerCase();
                if (domain !== "unesp.br") {
                    return false;
                }

                if (isLoggedIn && (isOnLogin || isOnRegister)) {
                    return Response.redirect(
                        new URL("/", nextUrl as unknown as URL)
                    );
                }

                if (isOnRegister || isOnLogin) {
                    return true; // Always allow access to register and login pages
                }

                if (isOnChat) {
                    if (isLoggedIn) return true;
                    return false; // Redirect unauthenticated users to login page
                }

                if (isLoggedIn) {
                    return Response.redirect(
                        new URL("/", nextUrl as unknown as URL)
                    );
                }
            }
            return true;
        },
        async jwt({ token, user }) {
            if (user) {
                token.id = user.id;
            }

            return token;
        },
        async session({
            session,
            token,
        }: {
            session: ExtendedSession;
            token: any;
        }) {
            if (session.user) {
                session.user.id = token.id as string;
            }

            return session;
        },
        async signIn(params) {
            console.log("signin params", JSON.stringify(params, null, 4));
            const { user } = params;

            const email = user?.email;
            const domain = email?.split("@")[1].toLowerCase();
            if (domain !== "unesp.br") {
                return false;
            }
            debugger;
            if (email && user.id) {
                const currentUser = await getUserById(user.id!);
                console.log("currentUser", currentUser);
                if (currentUser.length === 0) {
                    const userCreated = await createUser(
                        user.id,
                        email!,
                        "password"
                    );
                    console.log("userCreated", userCreated);
                }
            }
            return true;
        },
    },
} satisfies NextAuthConfig;
