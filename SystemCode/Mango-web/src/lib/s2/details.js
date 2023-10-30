import { s2ApiKey } from "$lib/s2/config.server.js";

const desiredFields = [
    "url", "title", "authors", "year", "publicationVenue", 
    "abstract", "citationCount", "isOpenAccess", "tldr"
];

export async function fetchS2DetailsAPI(ids) {
    const query = desiredFields.join();
    
    const data = await fetch(
        `https://api.semanticscholar.org/graph/v1/paper/batch?fields=${query}`, {
            method: "POST",
            body: JSON.stringify({
                "ids": ids
            }),
            header: {
                "X-API-Key": s2ApiKey,
            }
        }
    ).then((response) => response.json()).catch((error) => {
        console.error("Failed to fetch data from S2 API:", error);
        return null;
    });

    return data;
}
