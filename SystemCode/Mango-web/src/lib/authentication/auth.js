import { get, writable } from 'svelte/store';
import { updateUserProfile } from "$lib/stores/profile.js";

import Pocketbase from "pocketbase";

export const pbURL = "http://localhost:8090";
const pb = new Pocketbase(pbURL);

export const loggedInOrNot = writable(false);

export async function resetLoginState(state) {
    loggedInOrNot.set(state);
}

export const userAuth = writable({});

export async function resetAuth(data) {
    userAuth.set(data);
}

const logAuthStore = () => {
    // after the above you can also access the auth data from the authStore
    console.log(pb.authStore.isValid);
    console.log(pb.authStore.token);
    console.log(pb.authStore.model.id);

    // "logout" the last authenticated model
    pb.authStore.clear();
}

export async function loginAuth(email, password) {
    let isUserOrAdmin = false;

    // login with user
    try {
        const authData = await pb.collection('users')
            .authWithPassword(email, password);
        
        console.log("User login successful.")
        isUserOrAdmin = true;
        loggedInOrNot.set(true);
        // set user auth data into the writable
        const newAuthData = {
            token: authData.token,
            info: authData.record
        }
        resetAuth(newAuthData);
        // update user profile
        const updateResults = await updateUserProfile(
            newAuthData.info.id, newAuthData.token
        );
        console.log("updateResults: ", updateResults);
        // Log auth store
        logAuthStore();
    } catch (error) {
        console.log('Error:', error);
        console.log("User login failed. Trying admin login...");
    }

    // login with admin
    if(!isUserOrAdmin) {
        try {
            const authData = await pb.admins
                .authWithPassword(email, password);
            
            console.log("Admin login successful.")
            isUserOrAdmin = true;
            loggedInOrNot.set(true);
            // set admin auth data into the writable
            const newAuthData = {
                token: authData.token,
                info: authData.admin
            }
            resetAuth(newAuthData);
            // update user profile
            const updateResults = await updateUserProfile(
                newAuthData.info.id, newAuthData.token
            );
            console.log("updateResults: ", updateResults);
            // Log auth store
            logAuthStore();
        } catch (error) {
            console.log('Error:', error);
            console.log("Admin login failed. Please try again.")
        }
    }

    return isUserOrAdmin;
}

export async function refreshAuth() {
    const loginState = get(loggedInOrNot);
    if(!loginState) {
        return false;
    }
    
    const authData = get(userAuth);

    try {
        const response = await fetch(`${pbURL}/api/collections/users/auth-refresh`, {
            method: 'POST',
            headers: {
                'Authorization': authData.token
            },
        });
        const newAuthData = await response.json();
        
        resetAuth({
            record: newAuthData.record,
            token: newAuthData.token
        });
    } catch (error) {
        console.error(error);
    }

    return get(loggedInOrNot);
}

export async function logoutAuth() {
    await resetAuth({});

    await resetLoginState(false);

    return true;
}