import { get } from 'svelte/store';
import { loggedInOrNot, refreshAuth } from '$lib/authentication/auth.js';
import { goto } from '$app/navigation';

export async function load() {
    const loggedIn = get(loggedInOrNot);

    if (loggedIn) {
        refreshAuth();
        goto('/', { replaceState: true });
    }
}