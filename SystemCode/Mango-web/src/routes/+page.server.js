import { get } from "svelte/store";
import { refreshAuth, loggedInOrNot } from "$lib/authentication/auth.js";
import { fetchMangoRecommendAPI } from "$lib/mango/recommend.server.js";
import { userProfile } from "$lib/stores/profile.js";


export async function load() {
    const loggedIn = get(loggedInOrNot);
    const requestUserId = get(userProfile);
    console.log("userProfile: ", requestUserId);
    console.log(`Request for recommendation from '/' page.server.js: ${requestUserId}`);

    const paperRecommendations = async () => {
        return await fetchMangoRecommendAPI(requestUserId);
    }
    const refresh = async () => {
        return await refreshAuth();
    }

	return {
        loginState: loggedIn,
        papers: paperRecommendations(),
        refresh: refresh()
    };
}
