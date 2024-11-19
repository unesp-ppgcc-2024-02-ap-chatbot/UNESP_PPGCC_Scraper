import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Image from "next/image";

export default async function Page() {
    const membrosDaEquipe = [
        {
            nome: "André da Fonseca Schuck",
            lattes: "http://lattes.cnpq.br/3687175861120007",
            linkedin: "https://www.linkedin.com/in/andre-schuck",
            orientador: {
                nome: "João Paulo Papa",
                lattes: "http://lattes.cnpq.br/9039182932747194",
                linkedin:
                    "https://www.linkedin.com/in/jo%C3%A3o-paulo-papa-1a827923/",
            },
        },
        {
            nome: "Gabriel de Souza Lima",
            lattes: "http://lattes.cnpq.br/2789715683983963",
            linkedin: "https://www.linkedin.com/in/gabriel-lima-b3976b192",
            orientador: {
                nome: "Veronica Oliveira de Carvalho",
                lattes: "http://lattes.cnpq.br/1961581092362881",
            },
        },
        {
            nome: "Wagner Costa Santos",
            lattes: "http://lattes.cnpq.br/8724697279191424",
            linkedin: "https://www.linkedin.com/in/wagnercostasantos",
            orientador: {
                nome: "Arnaldo Candido Junior",
                lattes: "http://lattes.cnpq.br/8769928331729891",
            },
        },
    ];

    const docenteDisciplina = {
        nome: "Denis Henrique Pinheiro Salvadeo",
        lattes: "http://lattes.cnpq.br/1475921082905793",
        linkedin: "https://www.linkedin.com/in/denis-salvadeo-4022b88/",
    };

    const tecnologias = [
        {
            nome: "Qdrant",
            link: "https://qdrant.tech/",
            descricao:
                "Motor de busca vetorial para recuperação eficiente de informações similares.",
        },
        {
            nome: "Next.js",
            link: "https://nextjs.org/",
            descricao:
                "Framework React para construção de aplicações web modernas e otimizadas.",
        },
        {
            nome: "AI SDK (Vercel)",
            link: "https://sdk.vercel.ai/",
            descricao:
                "Kit de desenvolvimento para integração de IA em aplicações web.",
        },
        {
            nome: "Llama 3.2 11B",
            link: "https://ai.meta.com/llama/",
            descricao:
                "Modelo de linguagem Open Source usado para experimentos.",
        },
        {
            nome: "GPT-4o mini",
            link: "https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/",
            descricao: "Modelo de linguagem da OpenAI usado no chatbot.",
        },
        {
            nome: "BAAI/bge-m3",
            link: "https://huggingface.co/BAAI/bge-m3",
            descricao: "Modelo de embeddings para busca semântica avançada.",
        },
    ];

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="flex flex-col md:flex-row items-center justify-between mb-6">
                <Link
                    href="/"
                    className="px-4 py-2 rounded-lg bg-blue-500 hover:bg-blue-600 text-white transition-colors flex items-center space-x-2"
                >
                    <span>← Voltar para o Chatbot</span>
                </Link>
                <div className="grow text-center">
                    <h1 className="text-4xl font-bold">
                        Chatbot - UNESP (PPGCC) 🚀
                    </h1>
                </div>
                <Image
                    className="mt-4 md:mt-0"
                    src="/images/unesp.svg"
                    alt="Logo"
                    width={137}
                    height={55}
                />
            </div>

            <Card className="mb-8">
                <CardContent className="pt-6">
                    <h2 className="text-2xl font-semibold mb-4">
                        Visão Geral do Projeto 🎓
                    </h2>
                    <p className="text-lg mb-4">
                        Bem-vindo! Este é um projeto de chatbot, desenvolvido
                        como parte da disciplina de Aprendizado Profundo no{" "}
                        <Link
                            target="_blank"
                            className="text-blue-500 hover:underline"
                            href="https://www.ibilce.unesp.br/#!/pos-graduacao/programas-de-pos-graduacao/ciencia-da-computacao/apresentacao/"
                        >
                            Programa de Pós-Graduação em Ciência da Computação
                            (PPGCC) da UNESP!
                        </Link>{" "}
                        🤖💬
                    </p>
                    <p className="text-lg mb-4">
                        Este chatbot utilza aprendizado baseado em contexto
                        usando RAG (Geração Aumentada por Recuperação) para
                        responder perguntas sobre o programa PPGCC. Utilizamos
                        dados do site do PPGCC para criar um assistente
                        inteligente e responsivo para consultas relacionadas ao
                        programa.
                    </p>
                    <p className="text-lg">
                        É utilizado um sistema de busca híbrida. Este sistema
                        combina a busca semântica usando o modelo de embeddings{" "}
                        <Link
                            href="https://huggingface.co/BAAI/bge-m3"
                            className="text-blue-500 hover:underline"
                            target="_blank"
                        >
                            BAAI/bge-m3
                        </Link>{" "}
                        com o BM25. Após as buscas, utilizamos o{" "}
                        <Link
                            target="_blank"
                            href="https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf"
                            className="text-blue-500 hover:underline"
                        >
                            RRF (Reciprocal Rank Fusion)
                        </Link>{" "}
                        para combinar os resultados 🔍🧠
                    </p>
                </CardContent>
            </Card>

            <Card className="mb-8">
                <CardContent className="pt-6">
                    <h2 className="text-2xl font-semibold mb-4">
                        Disciplina: Aprendizado Profundo
                    </h2>
                    <div className="p-4 rounded-lg border">
                        <h3 className="text-xl">
                            Docente:{" "}
                            <span className="ml-1 font-semibold">
                                Prof. {docenteDisciplina.nome}
                            </span>
                        </h3>
                        <div className="flex space-x-2">
                            <Link
                                target="_blank"
                                href={docenteDisciplina.lattes}
                                className="text-blue-500 hover:underline"
                            >
                                Lattes
                            </Link>
                            <span className="text-gray-500">-</span>
                            <Link
                                target="_blank"
                                href={docenteDisciplina.linkedin}
                                className="text-blue-500 hover:underline"
                            >
                                LinkedIn
                            </Link>
                        </div>
                    </div>
                    <h2 className="text-2xl font-semibold mb-4 mt-8">
                        Alunos do Projeto 👥
                    </h2>
                    <div className="grid grid-cols-1 gap-4 mb-6">
                        {membrosDaEquipe.map((membro, index) => (
                            <div key={index} className="border p-4 rounded-lg">
                                <h3 className="text-xl font-semibold">
                                    {membro.nome}
                                </h3>
                                <div className="flex space-x-2">
                                    <Link
                                        target="_blank"
                                        href={membro.lattes}
                                        className="text-blue-500 hover:underline"
                                    >
                                        Lattes
                                    </Link>
                                    <span className="text-gray-500">-</span>
                                    <Link
                                        target="_blank"
                                        href={membro.linkedin}
                                        className="text-blue-500 hover:underline"
                                    >
                                        LinkedIn
                                    </Link>
                                </div>
                                <p className="text-gray-600 mb-2 dark:text-gray-300">
                                    Orientador:{" "}
                                    <span className="font-semibold">
                                        Prof. {membro.orientador.nome}
                                    </span>
                                    {" ("}
                                    <Link
                                        target="_blank"
                                        href={membro.orientador.lattes}
                                        className="text-blue-500 hover:underline"
                                    >
                                        Lattes
                                    </Link>
                                    {membro.orientador.linkedin && (
                                        <>
                                            <span className="ml-2">-</span>
                                            <Link
                                                target="_blank"
                                                href={
                                                    membro.orientador.linkedin
                                                }
                                                className="text-blue-500 hover:underline ml-2"
                                            >
                                                LinkedIn
                                            </Link>
                                        </>
                                    )}
                                    {")"}
                                </p>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardContent className="pt-6">
                    <h2 className="text-2xl font-semibold mb-4">
                        Tecnologias Utilizadas 💻
                    </h2>
                    <ul className="space-y-2">
                        {tecnologias.map((tech, index) => (
                            <li key={index} className="flex items-center">
                                <Badge
                                    variant="secondary"
                                    className="text-lg py-1 px-2 mr-2"
                                >
                                    <Link
                                        target="_blank"
                                        href={tech.link}
                                        className="hover:underline"
                                    >
                                        {tech.nome}
                                    </Link>
                                </Badge>
                                <span className="text-gray-700 dark:text-gray-300">
                                    {tech.descricao}
                                </span>
                            </li>
                        ))}
                    </ul>
                </CardContent>
            </Card>
        </div>
    );
}
