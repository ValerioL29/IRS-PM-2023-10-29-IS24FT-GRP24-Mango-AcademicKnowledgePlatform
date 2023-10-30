import { writable } from "svelte/store";

// true = light theme, false = dark theme
export const theme = writable(true);

export function changeTheme(new_value) {
  theme.set(new_value);
}

