import { writable } from "svelte/store";

export const rawSearchToken = writable("😎 Search for papers, authors, or topics");

export function updateSearchToken(token) {
    rawSearchToken.set(token);
}