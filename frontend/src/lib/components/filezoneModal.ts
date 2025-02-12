import type { ModalSettings } from "@skeletonlabs/skeleton";
import { goto } from "$app/navigation"

export const noFileErrorModal: ModalSettings = {
    type:"alert",
    title:"파일이 선택되지 않았습니다.",
    body:"pdf 파일을 업로드 하기 위해서는 먼저 파일을 업로드해야합니다.",
    buttonTextCancel: "확인",
}
 
export const fileUploadErrorModal: ModalSettings = {
    type:"alert",
    title:"파일 업로드에 실패했습니다.",
    body:"파일 업로드에 실패했습니다. 다시 시도해주세요.",
    buttonTextCancel: "확인",
    response: () => { goto("/hub")}
}

export const fileUploadSuccessModel: (document_id : string) => 
    ModalSettings = (document_id) => {
        return {
            type:"confirm",
            title:"파일 업로드 성공",
            body:"파일 업로드에 성공했습니다. 뷰어로 이동하시겠습니까?",
            buttonTextConfirm: "확인",
            buttonTextCancel: "돌아가기",
            response: () => { goto(`/viewer/${document_id}`)}
        }
    }
