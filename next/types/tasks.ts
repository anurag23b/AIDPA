export type Task = {
  id?: string;
  title: string;
  description?: string;
  schedule?: string;
  completed?: boolean;
  priority?: string;
  category?: string;
  due_date?: string; // ISO string
  repeat?: "none" | "daily" | "weekly" | "monthly";
  tags?: string[];
};
