import 'server-only'
import { createOpenAI } from '@ai-sdk/openai'
const apiServer = process.env.API_SEARCH_SERVER
const fireworks = createOpenAI({
  apiKey: process.env.FIREWORKS_API_KEY ?? '',
  baseURL: 'https://api.fireworks.ai/inference/v1'
})
const assistantPrompt = `You are an assistant for answering questions about the pos-graduate program in Computer Science at UNESP. 
Use the provided context information to answer the question. 
If you don't know the answer, simply state that you don't know.
Read all context carefully before answering.`

import {
  BotCard,
  BotMessage,
} from '@/components/chat-components'

import {
  createAI,
  createStreamableUI,
  getMutableAIState,
  getAIState,
  streamUI,
  createStreamableValue
} from 'ai/rsc'
import { openai } from '@ai-sdk/openai'



import {
  nanoid
} from '@/lib/utils'
import { saveChat } from '@/app/actions'
import { Chat, Message } from '@/lib/types'
import { auth } from '@/auth'
import { SpinnerMessage, UserMessage } from '@/components/chat-components/message'
import { generateText } from 'ai'

async function enrichPrompt(content: string) {
  const { text } = await generateText({
    model: openai('gpt-4o-mini'),
    // model: fireworks('accounts/fireworks/models/llama-v3p2-11b-vision-instruct'),
    prompt: `Create a bullet list with 5 alternative questions for the following text: ${content}. 
    If the text is not a question, you can rephrase it as a question and try to replace certain 
    words with synonyms to make it more diverse. If you don't know how to rephrase it, simply return an empty text.
    Always return in brazilian portuguese.
    `,
  });
  return text
}


async function submitUserMessage(content: string) {
  'use server'
  const aiState = getMutableAIState<typeof AI>()

  // const enrichedPrompt = await enrichPrompt(content)
  // console.log('Enriched prompt:', enrichedPrompt)
  const resultsPages = await fetch(`${apiServer}/api/search?q=${content}&result_limit=5&filter_type=page`)
  const pagesData = await resultsPages.json()
  const resultsDocs = await fetch(`${apiServer}/api/search?q=${content}&result_limit=5&filter_type=document`)
  const docsData = await resultsDocs.json()

  const topResultsContentPage = (pagesData.result || []).map((result: any) => result.content).join(' ')
  const topResultsContentDocs = (docsData.result || []).map((result: any) => result.content).join(' ')
  
  const topResultsContent = topResultsContentPage + topResultsContentDocs
  

  const prompt = `Instruction: ${assistantPrompt}
  ----Start of user question----
  ${content}
  ----End of user question----
  ----Start of context----
  ${topResultsContent}
  ----End of context----
  `

  aiState.update({
    ...aiState.get(),
    messages: [
      ...aiState.get().messages,
      {
        id: nanoid(),
        role: 'user',
        content: prompt
      }
    ]
  })
  let textStream: undefined | ReturnType<typeof createStreamableValue<string>>
  let textNode: undefined | React.ReactNode

  const result = await streamUI({
    model: openai('gpt-4o-mini'),
    // model: fireworks('accounts/fireworks/models/llama-v3p2-11b-vision-instruct'),    
    // model: fireworks('accounts/fireworks/models/phi-3-vision-128k-instruct'),        
    initial: <SpinnerMessage />,
    // system: `\
    // You are an assistant for answering questions about the graduate program in Computer Science at UNESP. Use the provided context information to answer the question. If you don't know the answer, simply state that you don't know. Keep your response concise, with a maximum of three sentences.
    // `,
    messages: [
      ...aiState.get().messages.map((message: any) => ({
        role: message.role,
        content: message.content,
        name: message.name
      }))
    ],
    text: ({ content, done, delta }) => {
      if (!textStream) {
        textStream = createStreamableValue('')
        textNode = <BotMessage content={textStream.value} />
      }

      if (done) {
        textStream.done()
        aiState.done({
          ...aiState.get(),
          messages: [
            ...aiState.get().messages,
            {
              id: nanoid(),
              role: 'assistant',
              content
            }
          ]
        })
      } else {
        textStream.update(delta)
      }

      return textNode
    }
  })

  return {
    id: nanoid(),
    display: result.value
  }
}

export type AIState = {
  chatId: string
  messages: Message[]
}

export type UIState = {
  id: string
  display: React.ReactNode
}[]

export const AI = createAI<AIState, UIState>({
  actions: {
    submitUserMessage
  },
  initialUIState: [],
  initialAIState: { chatId: nanoid(), messages: [] },
  onGetUIState: async () => {
    'use server'
    return undefined
    // const session = await auth()

    // if (session && session.user) {
    //   const aiState = getAIState() as Chat

    //   if (aiState) {
    //     const uiState = getUIStateFromAIState(aiState)
    //     return uiState
    //   }
    // } else {
    //   return
    // }
  },
  onSetAIState: async ({ state, done }) => {
    'use server'

    if (!done) return
    return
    // const session = await auth()
    // if (!session || !session.user) return

    // const { chatId, messages } = state

    // const createdAt = new Date()
    // const userId = session.user.id as string
    // const path = `/chat/${chatId}`

    // const firstMessageContent = messages[0].content as string
    // const title = firstMessageContent.substring(0, 100)

    // const chat: Chat = {
    //   id: chatId,
    //   title,
    //   userId,
    //   createdAt,
    //   messages,
    //   path
    // }

    // await saveChat(chat)
  }
})

export const getUIStateFromAIState = (aiState: Chat) => {
  return aiState.messages
    .filter(message => message.role !== 'system')
    .map((message, index) => ({
      id: `${aiState.chatId}-${index}`,
      display:
        message.role === 'tool' ? (
          message.content.map(tool => {
            return tool.toolName === 'listStocks' ? (
              <BotCard>
                {/* TODO: Infer types based on the tool result*/}
                {/* @ts-expect-error */}
                <Stocks props={tool.result} />
              </BotCard>
            ) : tool.toolName === 'showStockPrice' ? (
              <BotCard>
                {/* @ts-expect-error */}
                <Stock props={tool.result} />
              </BotCard>
            ) : tool.toolName === 'showStockPurchase' ? (
              <BotCard>
                {/* @ts-expect-error */}
                <Purchase props={tool.result} />
              </BotCard>
            ) : tool.toolName === 'getEvents' ? (
              <BotCard>
                {/* @ts-expect-error */}
                <Events props={tool.result} />
              </BotCard>
            ) : null
          })
        ) : message.role === 'user' ? (
          <UserMessage>{message.content as string}</UserMessage>
        ) : message.role === 'assistant' &&
          typeof message.content === 'string' ? (
          <BotMessage content={message.content} />
        ) : null
    }))
}
