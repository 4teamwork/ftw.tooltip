<tal:def define="ftwtooltips view/generate_tooltip_js_source">
var ftwtooltips = <span tal:replace="ftwtooltips" />;

function ShowTooltip(item){
    jq(item.selector).live('mouseover', function(e){
        e.preventDefault();
        var $this = jq(this);
        if (item.text){
            $this.attr('title', item.text);
        }
        if ($this.attr('title')){
            var customconfig = <span tal:replace="structure view/get_custom_config" />;
            var settings = jq.extend({
                tipClass:'',
                delay:0,
                cancelDefault: true,
                layout: "<span tal:replace="structure view/get_tooltip_layout" />",
                events: {
                    def: "mouseenter,mouseleave mousedown",
                    tooltip: 'mouseleave'
                }
            }, customconfig);

            $this.tooltip(settings);
            // Manually remove title attribute (live event allways readds the title attr)
            $this.attr('title', '');
            $this.trigger('mouseover')
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