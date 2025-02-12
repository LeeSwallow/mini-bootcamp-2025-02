<script>
    import { onMount } from 'svelte';
    import { fade } from 'svelte/transition';
    
    let visible = false;
    
    onMount(() => {
        visible = true;
    });
</script>

{#if visible}
<section transition:fade={{duration: 100}} class="container mx-auto px-4 py-16">
    <div class="text-center mb-16">
        <h1 class="text-4xl font-bold mb-4">AI 문서 요약 서비스</h1>
        <p class="text-xl text-gray-600 dark:text-gray-400">복잡한 문서를 쉽고 빠르게 이해하세요</p>
    </div>

    <div class="grid md:grid-cols-3 gap-8 mb-16">
        <div  class="card p-6 text-center">
            <div class="text-3xl mb-4">📄</div>
            <h3  class="text-xl font-semibold mb-2">PDF 업로드</h3>
            <p>PDF 문서를 드래그 앤 드롭으로 간편하게 업로드하세요</p>
        </div>
        <div class="card p-6 text-center">
            <div class="text-3xl mb-4">🔍</div>
            <h3 class="text-xl font-semibold mb-2">페이지 선택</h3>
            <p>원하는 페이지를 선택하여 필요한 부분만 요약할 수 있습니다</p>
        </div>
        <div class="card p-6 text-center">
            <div class="text-3xl mb-4">🤖</div>
            <h3 class="text-xl font-semibold mb-2">AI 요약</h3>
            <p>최신 AI 기술로 문서의 핵심 내용을 빠르게 파악하세요</p>
        </div>
    </div>

    <div class="text-center">
        <a href="/hub" class="btn variant-ghost-primary btn-xl">시작하기</a>
    </div>
</section>
{/if}

<style>
    :global(.card) {
        animation: fadeIn 1.5s ease-out;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>
