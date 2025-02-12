<script lang="ts">
    const docs: any = []
    for (let i = 0; i < 10; i++) {
        docs.push({
            title: `Document ${i + 1}`,
            thumbnail: "/pdf_icon.png"
        })
    }

</script>

<section class="flex px-6 py-8 w-full">
<div class="w-full bg-white rounded-lg shadow dark:border dark:bg-surface-800 dark:border-gray-700 flex flex-col">

<div class="p-6 sm:p-8">
    <h1 class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white mx-auto">
        PDF Viewer
    </h1>

    

<div class="my-6 flex flex-wrap">
    {#each docs as doc}
        <div class="w-1/2 sm:w-1/3 md:w-1/4 lg:w-1/5 xl:w-1/6">
            <a href="@">
            <div class="bg-gray-100 m-3 p-4 rounded-lg shadow hover:bg-gray-200 dark:bg-surface-600 dark:border dark:hover:bg-surface-400 dark:border-gray-700">
            <img src={doc.thumbnail} alt={doc.title} class="w-full h-auto object-cover mb-2"/>
            <h2 class="text-lg font-semibold">{doc.title}</h2>
            </div>
            </a>
        </div>
    {/each}
</div>

</div>
</section>