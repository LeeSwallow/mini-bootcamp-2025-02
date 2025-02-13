import { goto } from '$app/navigation';
import { user_id } from '$lib/stores/user';
import { token } from '$lib/stores/token';
import type { ModalSettings } from '@skeletonlabs/skeleton';

export const ConfirmSignUpModal: ModalSettings = {
    type: 'alert',
    title: '회원가입 성공',
    body: '회원가입이 완료되었습니다.\n 홈 화면으로 이동합니다.',
    buttonTextCancel: '확인',

    response: () => {
        goto('/');
    }
}

export const ConfirmEditProfileModal: ModalSettings = {
    type: 'alert',
    title: '프로필 수정 성공',
    body: '프로필 수정이 완료되었습니다.\n 로그인인 화면으로 이동합니다.',
    buttonTextCancel: '확인',

    response: () => {
        goto('/login').then(() => {
            user_id.set('');
            token.set('');
        });
    }
}

export const NoFileErrorModal: ModalSettings = {
    type:"alert",
    title:"파일이 선택되지 않았습니다.",
    body:"pdf 파일을 업로드 하기 위해서는 먼저 파일을 업로드해야합니다.",
    buttonTextCancel: "확인",
}
 
export const FileUploadErrorModal: ModalSettings = {
    type:"alert",
    title:"파일 업로드에 실패했습니다.",
    body:"파일 업로드에 실패했습니다. 다시 시도해주세요.",
    buttonTextCancel: "확인",
    response: () => { goto("/hub")}
}

export const LoadingModal: ModalSettings = {
    type:"alert",
    title:"로딩중",
    body:"잠시만 기다려주세요.",
    image: "/images/loading-bad.gif",
    buttonTextCancel: "",
}
