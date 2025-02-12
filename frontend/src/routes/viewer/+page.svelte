<script>
    import { onMount } from 'svelte';
    import SvelteMarkdown from 'svelte-markdown'
    let source = ""

    const clickEvent = () => {
        source += "## Hello World\n## Hello World\n## Hello World\n## Hello World\n## Hello World\n## Hello World\n## Hello World\n## Hello World\n";
        console.log("clicked");
    }

</script>

<section class="grid grid-cols-1 md:grid-cols-2 gap-4 px-6 py-8">
    <div class="bg-white rounded-lg shadow dark:border dark:bg-surface-800 dark:border-gray-700 p-4 h-screen flex flex-col">
        <!-- Header -->
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold">PDF Viewer</h2>
            <div class="text-sm text-gray-500">Page 1 of 10</div>
        </div>
        <!-- Viewer -->
        <div class="card p-4 rounded-lg bg-gray-100 dark:bg-surface-600 overflow-y-scroll flex-grow">
            <SvelteMarkdown {source} />
        </div>
        <!-- Footer -->
        <div class="flex justify-between mt-4 space-x-2">
            <button class="flex-1 px-4 py-2 btn variant-ghost-secondary">
            Prev
            </button>
            <button class="flex-1 px-4 py-2 btn variant-ghost-primary">
            Select
            </button>
            <button class="flex-1 px-4 py-2 btn variant-ghost-secondary">
            Next
            </button>
        </div>
    </div>
    <div class="bg-white rounded-lg shadow dark:border dark:bg-surface-800 dark:border-gray-700 p-4 h-screen flex flex-col">
        <!-- Header -->
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold">PDF Viewer</h2>
            <div class="text-sm text-gray-500">Page 1 of 10</div>
        </div>
        <!-- Viewer -->
        <div class="card p-4 rounded-lg bg-gray-100 dark:bg-surface-600 overflow-y-scroll flex-grow">
            <SvelteMarkdown {source} />
        </div>
        <!-- Footer -->
        <div class="flex justify-between mt-4 space-x-2">
            <button on:click={clickEvent} class="flex-1 px-4 py-2 btn variant-ghost-primary">
            Summarize
            </button>
        </div>
    </div>
</section>
<style lang="postcss">
</style>