import { writable } from "svelte/store";
import { pbURL } from "$lib/authentication/auth";

export const userProfile = writable("0049278456474afd8318df927a6905a1");

export async function updateUserProfile(userIdInPb, authToken) {
    const data = await fetch(
        `${pbURL}/api/collections/profiles/records?filter=(user_id='${userIdInPb}')`, {
            method: 'GET',
            headers: {
                'Authorization': authToken
            }
        }
    ).then(res => res.json()).catch(err => console.error(err));
    
    // set user profile data into the writable
    const newUUID = data?.items[0]?.uuid;
    userProfile.set(newUUID);

    return newUUID;
}