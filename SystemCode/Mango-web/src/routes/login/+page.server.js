import { get } from 'svelte/store';
import { loginAuth, logoutAuth, loggedInOrNot, refreshAuth, resetLoginState } from '$lib/authentication/auth.js';
import { redirect } from '@sveltejs/kit';


export async function load() {
    const loggedIn = get(loggedInOrNot);

    if (loggedIn) {
        await refreshAuth();
        console.log("You've signed in. Redirecting to home page...");

        throw redirect(308, '/');
    }
}

export const actions = {
    login: async ({ request }) => {
        // login with email and password
        const data = await request.formData();
		const email = data.get('email');
		const password = data.get('password');
        console.log("email: ", email);
        console.log("password: ", password);
        const isUserOrAdmin = await loginAuth(email, password);

        // login failed, fly in a toast to notify user
        if(isUserOrAdmin) {
            await resetLoginState(true);
            console.log("Login successfully. Redirecting to home page...");

            throw redirect(308, '/');
        } else {
            alert("Login failed. Please try again.");
        }

        return { success: true };
    },
    logout: async () => {
        const result = await logoutAuth();
        console.log("Logout successfully. Redirect to homepage...")

        if(result) {
            throw redirect(308, '/');
        } else {
            alert("Logout failed. Please try again.");
        }

        return { success: true };
    }
}
