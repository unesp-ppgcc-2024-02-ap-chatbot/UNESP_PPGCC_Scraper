import { auth } from '@/auth'
import SignupForm from '@/components/signup-form'
import { Session } from '@/lib/types'
import { redirect } from 'next/navigation'

export default async function SignupPage() {
  const session = (await auth()) as Session

  if (session) {
    redirect('/')
  }

  return (
    <main className="flex flex-col p-4">
      <h1 className="text-2xl font-bold">Sign Up</h1>
      <p className="text-red-500">
        Already have an account?{' '}
        <a href="/login" className="text-blue-500">
          Log in
        </a>
      </p>
      {/* <SignupForm /> */}
    </main>
  )
}
