<script>
    import { onMount } from 'svelte';
    import { get } from 'svelte/store';
	import Search from '$lib/core/Search.svelte';
    import { theme, changeTheme } from '$lib/stores/theme.js';
    import { userAuth } from '$lib/authentication/auth.js';
	import { enhance } from '$app/forms';

    export let userData;
    export let loginOrNot;

    const userName = get(userAuth).info?.username;
    const bookmarks = userData?.bookmarks;
    const histories = userData?.histories;

    onMount(() => {
        updateTheme();
    });

    function updateTheme() {
        const themeValue = $theme;

        if (themeValue) {
            document.documentElement.setAttribute('data-theme', "emerald");
            changeTheme(true);
        }
        else {
            document.documentElement.setAttribute('data-theme', "night");
            changeTheme(false);
        }
    }
</script>

<div class="fixed top-0 left-0 w-full z-50">
    <div class="navbar bg-base-100 p-4 shadow-md w-full fixed left-0 top-0">
        <div class="navbar-start">
            <a class="btn btn-ghost normal-case text-xl" href="/">🥭 Mango</a>
            <div class="divider divider-horizontal pr-4" />
            <div class="w-full">
                <Search />
            </div>
        </div>
        
        <div class="navbar-end space-x-4">
            <div class="flex-none">
                <label class="btn btn-circle swap swap-rotate normal-case">
                    <!-- this hidden checkbox controls the state -->
                    <input type="checkbox" bind:checked={$theme} on:change={updateTheme} />
                    <!-- sun icon -->
                    <div class="swap-on fill-current">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
                        </svg>                          
                    </div>
                    <!-- moon icon -->
                    <div class="swap-off fill-current">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" />
                        </svg>                          
                    </div>
                </label>
            </div>
            <div class="flex-none">
                <div class="dropdown dropdown-end">
                    <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
                    <!-- svelte-ignore a11y-label-has-associated-control -->
                    <label tabindex="0" class="btn btn-outline btn-secondary rounded-btn normal-case">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 3.75V16.5L12 14.25 7.5 16.5V3.75m9 0H18A2.25 2.25 0 0120.25 6v12A2.25 2.25 0 0118 20.25H6A2.25 2.25 0 013.75 18V6A2.25 2.25 0 016 3.75h1.5m9 0h-9" />
                        </svg>
                        Bookmarks
                    </label>
                    {#if bookmarks != null }
                        <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
                        <ul tabindex="0"  class="menu dropdown-content z-[1] p-2 shadow bg-base-100 rounded-box w-52 mt-4">
                            {#each bookmarks as bookmark}
                                <li>{bookmark.title}</li>
                            {/each}
                        </ul>
                    {:else}
                        <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
                        <div tabindex="0" class="dropdown-content z-[1] card card-compact w-64 p-2 mt-6 shadow bg-secondary text-secondary-content">
                            <div class="card-body">
                              <h3 class="card-title">🙈 Oops!</h3>
                              <p>Bookmark folder is empty.</p>
                            </div>
                        </div>
                    {/if} 
                </div>            
            </div>
            <div class="flex-none">
                <div class="dropdown dropdown-end">
                    <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
                    <!-- svelte-ignore a11y-label-has-associated-control -->
                    <label tabindex="0" class="btn btn-outline btn-accent rounded-btn normal-case">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>                  
                        Histories
                    </label>
                    {#if bookmarks != null }
                        <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
                        <ul tabindex="0"  class="menu dropdown-content z-[1] p-2 shadow bg-base-100 rounded-box w-52 mt-4">
                            {#each histories as paper}
                                <li>{paper.title}</li>
                            {/each}
                        </ul>
                    {:else}
                        <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
                        <div tabindex="0" class="dropdown-content z-[1] card card-compact w-64 p-2 mt-6 shadow bg-accent text-accent-content">
                            <div class="card-body">
                              <h3 class="card-title">🙈 Oops!</h3>
                              <p>History folder is empty.</p>
                            </div>
                        </div>
                    {/if} 
                </div>            
            </div>
            {#if loginOrNot}
                <div class="dropdown dropdown-end">
                    <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
                    <!-- svelte-ignore a11y-label-has-associated-control -->
                    <label tabindex="0" class="btn btn-outline btn-ghost btn-circle avatar">
                        <!-- first two charactor -->
                        {userName ? userName.toUpperCase().slice(0, 2) : "👤"}
                    </label>
                    <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
                    <div tabindex="0" class="dropdown-content z-[1] card card-compact w-64 p-2 mt-6 shadow bg-neutral text-neutral-content">
                        <div class="card-body">
                            <form method="POST" action="/login?/logout" use:enhance>
                                <button class="btn">👋 Logout</button>
                            </form>
                        </div>
                    </div>
                </div>
            {:else}
                <a class="btn btn-outline btn-ghost normal-case" href="/login">Log In</a>
            {/if}
        </div>
    </div>
</div>
