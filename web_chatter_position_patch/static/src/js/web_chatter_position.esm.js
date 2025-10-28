import {FormCompiler} from "@web/views/form/form_compiler";
import {patch} from "@web/core/utils/patch";
import {append, setAttributes} from "@web/core/utils/xml";

patch(FormCompiler.prototype, {
    /**
     * @override
     */
    compile(node, params) {
        const res = super.compile(node, params);
        const chatterContainerHookXml = res.querySelector(
            ".o-aside"
        );
        if (!chatterContainerHookXml) {
            // No chatter, keep the result as it is
            return res;
        }
        const formSheetBgXml = res.querySelector(".o_form_sheet_bg");
        const parentXml = formSheetBgXml && formSheetBgXml.parentNode;
        if (!parentXml) {
            // Miss-config: a sheet-bg is required for the rest
            return res;
        }

        if (odoo.web_chatter_position === "sided") {
            setAttributes(chatterContainerHookXml, {
                "t-attf-class": `o-aside mt-4 mt-md-0`,
            });
        }
        return res;
    },
});
