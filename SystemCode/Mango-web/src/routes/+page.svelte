<script>
    import PaperCard from "$lib/core/PaperCard.svelte";
    import Foo from "$lib/core/Foo.svelte";
    import Nav from "$lib/core/Nav.svelte";
	
    export let data;

    let displayTrends = true;

    // change display content selecting between trends and for you
    function handleSwitchContent() {
        displayTrends = !displayTrends;
        console.log(displayTrends);
    }
</script>

<Nav placeholder="😎 Search for papers, authors, or topics" loginOrNot={data.loginState}/>


<div class="w-full h-full relative top-[80px] px-8 bg-base-200">
    <!-- <div class="join join-horizontal flex justify-center pt-8">
        <button class="btn btn-accent join-item" on:click={handleSwitchContent}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.362 5.214A8.252 8.252 0 0112 21 8.25 8.25 0 016.038 7.048 8.287 8.287 0 009 9.6a8.983 8.983 0 013.361-6.867 8.21 8.21 0 003 2.48z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 18a3.75 3.75 0 00.495-7.467 5.99 5.99 0 00-1.925 3.546 5.974 5.974 0 01-2.133-1A3.75 3.75 0 0012 18z" />
            </svg>              
            Trends
        </button>
        <button class="btn btn-secondary join-item" on:click={handleSwitchContent}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
            </svg>              
            For you
        </button>
    </div> -->
    <div class="grid grid-flow-row py-8 space-y-8">
        {#each data.papers as paper}
            <PaperCard paper={paper} />
        {/each}
    </div>

    <Foo />
</div>
