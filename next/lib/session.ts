export function getUserId(): string {
  if (typeof window === "undefined") return "anonymous";
  
  let id = localStorage.getItem("aidpa-user");
  if (!id) {
    id = `user-${Math.random().toString(36).substring(2, 10)}`;
    localStorage.setItem("aidpa-user", id);
  }
  return id;
}
