<script>
	import { goto } from "$app/navigation";
    import { rawSearchToken, updateSearchToken } from "$lib/stores/search.js";

    let rawInput;

    async function handleSearchInput(e) {
        if (e.key === "Enter") {
            // Remove leading and trailing whitespace and replace all whitespace with a dash
            const searchToken = rawInput.toLowerCase().trim().replace(/\s+/g, "-");
            // Update the search token
            updateSearchToken(rawInput);
            // Navigate to the search page
            goto(`/search/${searchToken}`, {
                replaceState: true
            });
        }
    }
</script>


<div class="relative">
    <input 
        type="text" bind:value={rawInput} 
        placeholder={$rawSearchToken}
        class="input input-bordered lg:w-full md:w-auto" 
        on:keydown={handleSearchInput}
    />
</div>

