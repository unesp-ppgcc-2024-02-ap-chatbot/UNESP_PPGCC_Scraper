import { createUser, getUser } from "@/lib/db/queries";
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
            console.log("jwt user", user);
            console.log("jwt token", token);
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
            console.log("session", session);
            console.log("session token", token);
            if (session.user) {
                session.user.id = token.id as string;
            }

            return session;
        },
        async signIn(params) {
            console.log("signin params", JSON.stringify(params, null, 4));
            const { user } = params;

            const email = user?.email;
            debugger;
            if (email && user.id) {
                const currentUser = await getUser(email!);
                if (currentUser.length === 0) {
                    await createUser(user.id, email!, "password");
                }
            }
            return true;
        },
    },
    // callbacks: {
    //   authorized(allData) {
    //     const { auth, request: { nextUrl } } = allData;
    //     debugger
    //     const isLoggedIn = !!auth?.user;
    //     const isOnChat = nextUrl.pathname.startsWith('/');
    //     const isOnRegister = nextUrl.pathname.startsWith('/register');
    //     const isOnLogin = nextUrl.pathname.startsWith('/login');

    //     if (isLoggedIn && (isOnLogin || isOnRegister)) {
    //       return Response.redirect(new URL('/', nextUrl as unknown as URL));
    //     }

    //     if (isOnRegister || isOnLogin) {
    //       return true; // Always allow access to register and login pages
    //     }

    //     if (isOnChat) {
    //       if (isLoggedIn) return true;
    //       return false; // Redirect unauthenticated users to login page
    //     }

    //     if (isLoggedIn) {
    //       return Response.redirect(new URL('/', nextUrl as unknown as URL));
    //     }

    //     return true;
    //   },
    // },
} satisfies NextAuthConfig;
