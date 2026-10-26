import type { Item, Source } from "@/lib/types";

const NOT_CITED = Number.MAX_SAFE_INTEGER;

export default function Content({ item }: { item: Item }) {
  const sources = [...item.sources].sort(
    (a, b) => (a.number ?? NOT_CITED) - (b.number ?? NOT_CITED),
  );

  return (
    <article className="rounded-lg bg-white p-6 text-slate-900 shadow-md">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
        {item.category.replaceAll("_", " ")}
      </p>

      <h3 className="mt-2 text-lg font-semibold">{item.question}</h3>

      <div
        className="mt-4 border-t border-slate-200 pt-4 leading-relaxed whitespace-pre-line [&_a]:font-semibold [&_a]:text-[#004b88] [&_a]:underline [&_a:hover]:no-underline"
        dangerouslySetInnerHTML={{ __html: item.content }}
      />

      <h4 className="mt-6 text-xs font-semibold uppercase tracking-wide text-slate-500">
        Sources
      </h4>
      <ul className="mt-2 flex flex-col gap-2">
        {sources.map((source) => (
          <SourceRow key={source.id} source={source} />
        ))}
      </ul>
    </article>
  );
}

function SourceRow({ source }: { source: Source }) {
  const cited = source.number !== null;

  return (
    <li className={`flex items-center gap-3 ${cited ? "" : "opacity-60"}`}>
      {source.favicon && (
        <img src={source.favicon} alt="" width={16} height={16} className="shrink-0" />
      )}
      <a
        href={source.source}
        target="_blank"
        rel="noopener noreferrer"
        className="flex-1 text-[#004b88] hover:underline"
      >
        {source.title}
      </a>
      <span className="shrink-0 rounded bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-600">
        {cited ? `[${source.number}]` : "Not cited"}
      </span>
    </li>
  );
}