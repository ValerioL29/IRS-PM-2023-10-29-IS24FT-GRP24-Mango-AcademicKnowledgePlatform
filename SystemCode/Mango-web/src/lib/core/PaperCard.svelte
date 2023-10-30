<script>
    export let paper;
</script>

<div class="card lg:card-side bg-base-100 shadow-xl">
    <div class="card-body w-[70%] flex flex-col space-y-4">
        <h1 class="card-title row-span-1">
            {paper.title}
        </h1>
        <div class="flex flex-row space-x-4 items-center">
            {#if paper.venue}
                <h2 class="font-bold">{paper.venue}</h2>
            {/if}
            {#if paper.year}
                <span class="badge badge-secondary">{paper.year}</span>
            {/if}
        </div>
        <div>
            {#each paper.authors.slice(0, 5) as author}
                <div class="badge badge-outline">{author.name}</div>
            {/each}
            {#if paper.authors.length > 5}
                <div class="badge badge-outline">+{paper.authors.length - 5} more</div>
            {/if}
        </div>
        <h3 class="">
            {#if paper.tldr}
                <span class="badge badge-md">TLDR;</span>
                {paper.tldr.text}
            {:else if paper.details.abstract}
                {#if paper.details.abstract.split(' ').length > 100}
                    <span class="badge badge-md">Abstract</span>
                    {paper.details.abstract.split(' ').slice(0, 100).join(' ')}...
                {:else}
                    <span class="badge badge-md">Abstract</span>
                    {paper.details.abstract}
                {/if} 
            {:else}
                <div class="alert alert-info">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    <span>Sorry, we don't have any quick introduction of this essay.🥹</span>
                </div>
            {/if}
        </h3>
        <a class="btn btn-secondary" href="/paper/{paper.paperId}">
            Read!
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
            </svg>              
        </a>
    </div>
</div>

<style>
    .badge {
        margin-right: 0.5rem;
    }
    
    /* .card figure {
        width: 30%;
        height: 100%;
        object-fit: cover;
    } */
</style>