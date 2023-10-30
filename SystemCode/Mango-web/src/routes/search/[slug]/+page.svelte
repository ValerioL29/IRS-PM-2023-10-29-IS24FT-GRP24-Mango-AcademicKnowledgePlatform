<script>
    import Foo from "$lib/core/Foo.svelte";
    import Nav from "$lib/core/Nav.svelte";
	import PaperCard from "$lib/core/PaperCard.svelte";

    export let data;
    // const s2Results = data.s2;
    const searchResults = data.mango;
    // const searchResults = [].concat(s2Results, mangoResults);
</script>

<Nav placeholder="😎 Search for papers, authors, or topics" />

<div class="w-full h-full relative top-[80px] px-8">
    <h1 class="text-3xl font-bold pt-8">Search Results</h1>
    <div class="divider"></div>
    <div class="grid grid-flow-row py-8 space-y-8">
        {#if searchResults?.length > 0}
            {#each searchResults as result}
                <PaperCard paper={result} />
            {/each}
        {:else}
            <div class="alert">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-info shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span>Sorry. No results found for <b>'{data.query}'</b>. We are working on it. 🧑‍💻</span>
            </div>
        {/if}
    </div>
    <Foo />
</div>

