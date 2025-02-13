<script context="module">
    export { load } from './+page';
</script>

<script lang="ts">
    import { onMount } from 'svelte';
    import SvelteMarkdown from 'svelte-markdown';
    import { get } from 'svelte/store';
    import { token } from '$lib/stores/token';
    import { clipboard} from '@skeletonlabs/skeleton';
    import { ProgressRadial } from '@skeletonlabs/skeleton';
    import { fade } from 'svelte/transition';

    export let data;
    const { document, userId } = data;

    const pageConfig = {
        currentPage: 1,
        totalPages: (document?.num_page) ? document?.num_page : 0,
    }
    
    const imageConfig = {
        imageCache: new Map<number, string>(),
        loading: false,
        currentImageUrl: ""
    }

    const summaryConfig = {
        loading: false,
        source: "",
        mode: 0, // 0: none, 1: select(single), 2: select(multi)
        start: 0,
        end: 0,
        buttonText : "선택하기",
        buttonStyle : "btn variant-ghost-surface"
    }
    $: summaryConfig.buttonStyle = summaryConfig.mode === 0 ? "btn variant-ghost-surface" : (summaryConfig.mode === 1 ? "btn variant-ghost-primary" : "btn variant-ghost-success");
    $: summaryConfig.buttonText = summaryConfig.mode === 0 ? "선택하기" : (summaryConfig.mode === 1 ? `페이지 ${summaryConfig.start} 선택됨` : `페이지 ${summaryConfig.start} ~ ${summaryConfig.end} 선택됨`);

    let visible = false;

    onMount(async () => {
        visible = true;
        imageConfig.currentImageUrl = await loadImage(pageConfig.currentPage) || "";
        preloadImages(pageConfig.currentPage);
    });


    async function loadImage(pageNum: number) {
        if (imageConfig.imageCache.has(pageNum)) { return imageConfig.imageCache.get(pageNum); }
        try {
            imageConfig.loading = true;
            const res = await fetch(`/api/image/documents/pages?pageNum=${pageNum}`, {
                headers: { 'Authorization': `Bearer ${get(token)}` }
            });
            const blob = await res.blob();
            const url = URL.createObjectURL(blob);
            imageConfig.imageCache.set(pageNum, url);
            return url;
        } catch (error) {
            console.error('이미지 로딩 실패:', error);
            return null;
        } finally {
            imageConfig.loading = false;
        }
    }

    async function preloadImages(currentPageNum: number) {
        // 현재 페이지 주변 이미지 프리로드
        const pagesToPreload = [currentPageNum + 1, currentPageNum - 1]
            .filter(page => page > 0 && page <= pageConfig.totalPages);
        for (const pageNum of pagesToPreload) {
            if (!imageConfig.imageCache.has(pageNum)) {
                loadImage(pageNum);
            }
        }
    }

    async function changePage(direction: 'prev' | 'next') {
        const newPage = direction === 'next' ? 
            Math.min(pageConfig.currentPage + 1, pageConfig.totalPages) : 
            Math.max(pageConfig.currentPage - 1, 1);

        if (newPage !== pageConfig.currentPage) {
            pageConfig.currentPage = newPage;
            imageConfig.currentImageUrl = await loadImage(pageConfig.currentPage) || "";
            preloadImages(pageConfig.currentPage);
        }
    }

    function onSelect()  {
        if (summaryConfig.mode === 0) {
            summaryConfig.mode = 1; // 싱글 페이지 선택
            summaryConfig.start = pageConfig.currentPage;
        } else if (summaryConfig.mode === 1) {
            if (summaryConfig.start === pageConfig.currentPage) {
                summaryConfig.start = summaryConfig.end = summaryConfig.mode = 0; // 선택 해제
            } else {
                summaryConfig.mode = 2; // 멀티 페이지 선택
                summaryConfig.end = pageConfig.currentPage;
                if (summaryConfig.start > summaryConfig.end) {
                    const temp = summaryConfig.start;
                    summaryConfig.start = summaryConfig.end;
                    summaryConfig.end = temp;
                }
                summaryConfig.buttonText = `페이지 ${summaryConfig.start} ~ ${pageConfig.currentPage} 선택됨`;
            }
        } else if (pageConfig.currentPage >= summaryConfig.start && pageConfig.currentPage <= summaryConfig.end) {
            summaryConfig.start = summaryConfig.end = summaryConfig.mode = 0; // 선택 해제
        
        } else {
            summaryConfig.mode = 1; // 싱글 페이지 선택
            summaryConfig.start = pageConfig.currentPage;
        }
    }

    async function onSummarize() {
        summaryConfig.loading = true;
        let apiUrl = `/api/get/documents/${document?.id}/summary?startPage=${summaryConfig.start}`;
        if (summaryConfig.mode === 2) {
            apiUrl += `&endPage=${summaryConfig.end}`;
        }
        try {
            const res = await fetch(apiUrl, {
                headers: { 'Authorization': `Bearer ${get(token)}` }
            });
            const body = await res.json();
            summaryConfig.source = body.summary;
        } catch (error) {
            console.error('요약 데이터 로딩 실패:', error);
            summaryConfig.source = "# 요약 데이터를 불러올 수 없습니다";
        } finally {
            summaryConfig.loading = false;
        }
    }



</script>

{#if visible}
<section transition:fade={{duration: 1000}} class="grid grid-cols-1 md:grid-cols-2 gap-4 px-6 py-8">
    <div class="bg-white rounded-lg shadow dark:border dark:bg-surface-800 dark:border-gray-700 p-4 h-screen flex flex-col">
        <!-- Header -->
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold">PDF Viewer</h2>
            <div class="text-sm text-gray-500">Page {pageConfig.currentPage} of {pageConfig.totalPages}</div>
        </div>
        <!-- Viewer -->
        <div class="card p-4 rounded-lg bg-gray-100 dark:bg-surface-600 overflow-y-scroll flex-grow">
            {#if imageConfig.loading}
                <div class="flex justify-center items-center h-full">
                    <div class="loading"></div>
                </div>
            {:else if imageConfig.currentImageUrl}
                <img 
                    src={imageConfig.currentImageUrl} 
                    alt={`PDF Page ${pageConfig.currentPage}`}
                    class="w-full h-auto"
                />
            {:else}
                <div class="text-center">이미지를 불러올 수 없습니다</div>
            {/if}
        </div>
        <!-- Footer -->
        <div class="flex justify-between mt-4 space-x-2">
            <button 
                on:click={() => changePage('prev')} 
                class="flex-1 px-4 py-2 btn variant-ghost-secondary"
                disabled={pageConfig.currentPage === 1 || imageConfig.loading}
            >
                이전
            </button>
            <button 
                on:click={() => onSelect()} 
                class="flex-1 px-4 py-2 btn {summaryConfig.buttonStyle}"
            >
                {summaryConfig.buttonText}
            </button>
            <button 
                on:click={() => changePage('next')} 
                class="flex-1 px-4 py-2 btn variant-ghost-secondary"
                disabled={pageConfig.currentPage === pageConfig.totalPages || imageConfig.loading}
            >
                다음
            </button>
        </div>
    </div>
    <div class="bg-white rounded-lg shadow dark:border dark:bg-surface-800 dark:border-gray-700 p-4 h-screen flex flex-col">
        <!-- Header -->
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold">AI 요약</h2>
            <button class="btn variant-ghost-tertiary px-4 m-2" use:clipboard={summaryConfig.source}>복사하기</button>
            <div class="card p-4 variant-filled-primary" data-popup="copyPopup">
                <p>Click Content</p>
                <div class="arrow variant-filled-primary" />
            </div>
        </div>
        <!-- Viewer -->
        <div class="card p-4 rounded-lg bg-gray-100 dark:bg-surface-600 overflow-y-scroll flex-grow">
            {#if summaryConfig.loading}
            <div class="flex justify-center items-center h-full">
                <ProgressRadial size="large" stroke={100} meter="stroke-surface-500" track="stroke-surface-500/30" strokeLinecap="butt" value={undefined}/>
            </div>
            {:else}
                <SvelteMarkdown source={summaryConfig.source}  options = {{ breaks : true }}/>
            {/if}
        </div>
        <!-- Footer -->
        <div class="flex justify-between mt-4 space-x-2">
            <button on:click={onSummarize} class="flex-1 px-4 py-2 btn variant-ghost-primary"
                disabled={summaryConfig.loading || summaryConfig.mode === 0}>
                요약하기
            </button>
        </div>
    </div>
</section>
{/if}
<style lang="postcss">

[data-popup] {
	/* Display */
	display: none;
	/* Position */
	position: absolute;
	top: 0;
	left: 0;
	/* Transitions */
	transition-property: opacity;
	transition-timing-function: cubic-bezier(.4,0,.2,1);
	transition-duration: .15s
}
</style>

