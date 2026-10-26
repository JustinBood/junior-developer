import Image from "next/image";
import { Suspense } from "react";
import type { Item } from "@/lib/types";
import Content from "@/components/Content";

async function ContentList() {
  const res = await fetch("http://localhost:8000/data");
  if (!res.ok) {
    throw new Error(`Couldn't load the data: ${res.status}`);
  }
  const items: Item[] = await res.json();

  return (
    <div className="flex w-full flex-col gap-6">
      {items.map((item, index) => (
        <Content key={index} item={item} />
      ))}
    </div>
  );
}

export default function Home() {
  return (
    <main className="mx-auto flex max-w-3xl flex-col items-center gap-8 p-8">
      <div className="flex flex-col items-center text-center">
        <Image
          src="/logo.png"
          alt="Citizens Advice SORT"
          width={150}
          height={150}
          priority
        />
        <h1 className="mt-4 text-2xl font-bold">Citizens Advice SORT</h1>
        <h2 className="text-lg font-medium">Junior Developer Practical</h2>
      </div>
      {/* Anything that fetches data goes inside Suspense, which shows the fallback until it's ready */}
      <Suspense fallback={<p>Loading...</p>}>
        <ContentList />
      </Suspense>
    </main>
  );
}
