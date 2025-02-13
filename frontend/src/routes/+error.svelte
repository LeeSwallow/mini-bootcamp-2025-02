<script lang="ts">
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";

  let visible = false;

  onMount(() => {
    visible = true;
  });
</script>

{#if visible}
  <div
    transition:fade={{ duration: 100 }}
    class="flex items-center justify-center h-screen"
  >
    <div
      class="card text-center w-1/2 h-1/2 flex flex-col items-center justify-center"
    >
      <h1 class="text-4xl font-bold mb-4">
        {$page.status}: {$page.error?.message || "오류가 발생했습니다"}
      </h1>
      <p class="text-gray-600 dark:text-gray-400 mb-8">
        {#if $page.status === 404}
          요청하신 페이지를 찾을 수 없습니다.
        {:else}
          문제가 발생했습니다. 다시 시도해 주세요.
        {/if}
      </p>
      <a href="/" class="btn variant-ghost-primary">홈으로 돌아가기</a>
    </div>
  </div>
{/if}

<style>
  .card {
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
