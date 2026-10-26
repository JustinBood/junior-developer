export type Source = {
  id: string;
  title: string;
  source: string;
  number: number | null;
  favicon: string | null;
};

export type Item = {
  category: string;
  question: string;
  sources: Source[];
  content: string;
};