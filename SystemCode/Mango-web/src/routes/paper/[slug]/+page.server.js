import { get } from 'svelte/store';
import { loggedInOrNot } from '$lib/authentication/auth.js';
import { fetchMangoPaperAPI } from '$lib/mango/paper.server.js';
import { fetchMangoRecEmbeddingAPI } from '$lib/mango/recommend.server.js';
import { fetchMangoGraphAPI } from '$lib/mango/graph.server.js';

export async function load({ params }) {
    const loggedIn = get(loggedInOrNot);
    console.log("loggedIn: ", loggedIn);
    
    const slug = params.slug;
    const paperDetails = async () => {
        return await fetchMangoPaperAPI(slug);
    };
    const embeddingRecommendations = async () => {
        return await fetchMangoRecEmbeddingAPI(slug);
    }
    const graphDetails = async () => {
        return await fetchMangoGraphAPI(slug);
    }

    return {
        loginState: loggedIn,
        paper: paperDetails(),
        similar: embeddingRecommendations(),
        graph: graphDetails(),
    };
}