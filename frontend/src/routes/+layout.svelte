<script lang="ts">
	import '../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';

	// Highlight JS
	import hljs from 'highlight.js/lib/core';
	import 'highlight.js/styles/github-dark.css';
	import { storeHighlightJs } from '@skeletonlabs/skeleton';
	import xml from 'highlight.js/lib/languages/xml'; // for HTML
	import css from 'highlight.js/lib/languages/css';
	import javascript from 'highlight.js/lib/languages/javascript';
	import typescript from 'highlight.js/lib/languages/typescript';

	hljs.registerLanguage('xml', xml); // for HTML
	hljs.registerLanguage('css', css);
	hljs.registerLanguage('javascript', javascript);
	hljs.registerLanguage('typescript', typescript);
	storeHighlightJs.set(hljs);

	// Floating UI for Popups
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

	// Modal Store Setup
	import { initializeStores, Modal } from '@skeletonlabs/skeleton';
	initializeStores();

	// auth store
	import { setAuth, getAuth, removeAuth } from '$lib/stores/auth';
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';


	function logout() {
		removeAuth();
		
		goto('/');
	}
</script>
<!-- Modal -->
<Modal />
<!-- App Shell -->
<AppShell>
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar class="mb-4">
			<svelte:fragment slot="lead">
				<strong class="text-xl uppercase">
					My PDF Summarizer
				</strong>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				<button class="btn variant-ghost-surface" on:click={() => goto('/')}>홈</button>
				{#if getAuth().isLogin}
					<button class="btn variant-ghost-surface" on:click={ logout }>로그아웃</button>
					<button class="btn variant-ghost-surface" on:click={() => goto('/hub')}>마이페이지</button>
				{:else}
					<button class="btn variant-ghost-surface" on:click={() => goto('/login')}>로그인</button>
					<button class="btn variant-ghost-surface" on:click={() => goto('/signup')}>회원가입</button>
				{/if}

			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<!-- Page Route Content -->
	<slot />


</AppShell>
