<tal:def define="ftwtooltips view/generate_tooltip_js_source">
var ftwtooltips = <span tal:replace="ftwtooltips" />;

function ShowTooltip(item){
    jq(item.selector).live('mouseover', function(){
        var $this = jq(this);
        if (item.text){
            $this.attr('title', item.text);
        }
        if ($this.attr('title')){
            $this.tooltip({
                opacity: 0.7,
                layout: <span tal:replace="view/get_tooltip_layout" />;
            });
            $this.data('tooltip').show();
        }
    });
}

jq(function(){
    jq(ftwtooltips).each(function(i, o){
        if (jq(o.condition).length !== 0){
            ShowTooltip(o);
        }

    });
});
</tal:def>