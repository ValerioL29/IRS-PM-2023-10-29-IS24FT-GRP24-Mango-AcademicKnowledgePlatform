import { refreshAuth } from '$lib/authentication/auth.js';
import { fetchMangoSearchAPI } from '$lib/mango/search.server.js';
// import { fetchS2AutocompleteAPI } from '$lib/s2/autocomplete.js';

export async function load({ params }) {
    // Get the search token from the URL
    console.log("Running load function with slug: ", params.slug);
    const mangoSearchResults = async () => {
        return await fetchMangoSearchAPI(params.slug);
    }
    // const s2SearchResults = async () => {
    //     return await fetchS2AutocompleteAPI(params.slug);
    // }
    const refresh = async () => {
        return await refreshAuth();
    }

    return {
        query: params.slug,
        // s2: s2SearchResults(),
        mango: mangoSearchResults(),
        refresh: refresh()
    };
}
