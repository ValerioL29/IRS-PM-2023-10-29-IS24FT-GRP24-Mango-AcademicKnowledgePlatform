import { s2ApiKey } from "$lib/s2/config.server.js";
import { fetchS2DetailsAPI } from "$lib/s2/details.js";

export async function fetchS2AutocompleteAPI(token) {
    const apiURL = "https://api.semanticscholar.org/graph/v1/paper/autocomplete"
    const data = await fetch(
        `${apiURL}?query=${token}`, {
            method: "GET",
            headers: {
                "X-API-Key": s2ApiKey,
            },
        }
    ).then((response) => response.json())
    .catch((error) => {
        console.error("Failed to fetch data from S2 API:", error);
        return null;
    });

    const candidate_ids = data.matches.map((paper) => paper.id);
    const papers = await fetchS2DetailsAPI(candidate_ids);
    // Await for request limit
    await new Promise(resolve => setTimeout(resolve, 1000));
    // Check status
    if (papers?.length > 0) {
        console.log("Get papers from S2 API:", papers.length);
    }

    return papers;
}
