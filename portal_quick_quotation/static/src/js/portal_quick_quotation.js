/** @odoo-module */

import PublicWidget from "@web/legacy/js/public/public_widget";
import { debounce } from "@bus/workers/websocket_worker_utils";
import { _t } from "@web/core/l10n/translation";

export const createNewQuotation = PublicWidget.Widget.extend({
    selector: '#wrapwrap:has(.o_portal_quick_quotation)',    

    events: {
        "click .add-new": debounce(function (e) {
            this.add_new_row(e);
        }, 200, true),

        "click .add": debounce(function (e) {
            this.add_row(e);
        }, 200, true),

        "click .edit": debounce(function (e) {
            this.edit_row(e);
        }, 200, true),

        "click .delete": debounce(function (e) {
            this.delete_row(e);
        }, 200, true),

        "change input#product": debounce(function (e) {
            this.on_change_product(e);
        }, 200, true),

        "change .quantity": debounce(function (e) {
            this.on_change_quantity(e);
        }, 200, true),

        "click .submit": debounce(function (e) {
            this.on_click_submit(e);
        }, 200, true),

        "keyup .search_prodcuts" : "on_search_prodcuts",
    },
    
    init() {
        this._super(...arguments);
        this.rpc = this.bindService("rpc");
    },

    start: function () {
        var self = this;            
        return this._super.apply(this, arguments).then(function () {
            $('.submit').attr("disabled", "disabled");
            $('.search_prodcuts').attr("disabled", "disabled");

            $('input.salesperson').each(function(){
                if (!$(this).data('select2'))
                {                        
                    $(this).select2({
                        width: '100%',
                        placeholder: "Select salesperson",
                        allowClear: true,
                        formatNoMatches: _t('No results found'),
                        multiple: false,
                        minimumInputLength: 2,
                        selection_data: false,
                        fill_data: function (query, data) {
                            var that = this;
                            var tags = {results: []};
                            data.forEach((obj) => {
                                if (that.matcher(query.term, obj.name)) {
                                    tags.results.push({id: obj.id, text: obj.name});
                                }
                            })                            
                            query.callback(tags);
                        },
                        query: function (query) {
                            var that = this;
                            // fetch data only once and store it
                            if (!this.selection_data) {
                                self.rpc('/portal_quick_quotation/get_salespersons_data').then(function (data) {
                                    that.fill_data(query, data);
                                    that.selection_data = data;
                                });
                            } else {
                                this.fill_data(query, this.selection_data);
                            }
                        }
                    });                            
                }
            });
        })
    },

    add_new_row: function(e){      
        e.preventDefault();
        e.stopPropagation();
        var self = this;
        var $target = $(e.currentTarget);     
        $target.attr("disabled", "disabled");
        var index = $("table tbody tr:last-child").index();            
        this.actions = '<a class="add" title="Add" data-toggle="tooltip">' +
            '<i class="fa fa-check"></i>' + 
            '</a>' +
            '<a class="edit" title="Edit" data-toggle="tooltip">' +
            '<i class="fa fa-edit"></i>' +
            '</a>' +
            '<a class="delete" title="Delete" data-toggle="tooltip">' +
            '<i class="fa fa-trash"></i>' + 
            '</a>';            

        var row = "";
        row += '<tr>';
        row += '<td></td>';
        row += '<td><input type="text" class="form-control product" id="product" name="product"/></td>';
        row += '<td><span class="unit" name="unit" id="unit"></span></td>';
        row += '<td><input type="text" class="form-control quantity" name="quantity" id="quantity"></td>';
        row += '<td>' + this.actions + '</td>';
        row += '</tr>';

        $("table").append(row);		
        $("table tbody tr").eq(index + 1).find(".add, .edit").toggle();

        this.add_row_number($('#table_quick_quotation'));

        $("table[id='table_quick_quotation']").each(function() {
            $(this).find('input.product').each(function(){
                if (!$(this).data('select2'))
                {                        
                    $(this).select2({
                        width: '100%',
                        placeholder: "Select Product",
                        allowClear: true,
                        formatNoMatches: _t('No results found'),
                        multiple: false,
                        minimumInputLength: 2,
                        selection_data: false,
                        fill_data: function (query, data) {
                            var that = this;
                            var tags = {results: []};
                            data.forEach((obj) => {
                                if (that.matcher(query.term, obj.display_name)) {
                                    tags.results.push({id: obj.id, text: obj.display_name, uom_id: obj.uom_id});
                                }
                            })
                            query.callback(tags);
                        },
                        query: function (query) {
                            var that = this;
                            // fetch data only once and store it
                            if (!this.selection_data) {
                                self.rpc('/portal_quick_quotation/get_products_data').then(function (data) {
                                    that.fill_data(query, data);
                                    that.selection_data = data;
                                });
                            } else {
                                this.fill_data(query, this.selection_data);
                            }
                        }
                    });                            
                }
            });
        });
        
        this.check_row_number($('#table_quick_quotation'));
    },
    
    add_row_number:function($table) {
        var count = 0;
        $table.find("tbody tr").each(function(index, el) {
            $(el).find("td:eq(0)").html(++count + ".");
        });
    },

    check_row_number: function($table){
        var count = 0;
        $table.find("tbody tr").each(function(index, el) {
            count = count + 1;
        });
        if(count > 0){
            $('.submit').removeAttr("disabled");
            $('.search_prodcuts').removeAttr("disabled");
        }else{
            $('.submit').attr("disabled", "disabled");
            $('.search_prodcuts').attr("disabled", "disabled");
        }
    },  

    delete_row_number: function(e){
        e.preventDefault();
        var $target = $(e.currentTarget);
        var $row = $target.parents("tr");
        if ($row) {
            $row.remove();
            this.add_row_number($("#table_quick_quotation"));
        }
        this.check_row_number($('#table_quick_quotation'));
    },

    add_row: function(e){
        e.preventDefault();
        e.stopPropagation();
        
        var product_empty = false;
        var quantity_empty = false;

        var $target = $(e.currentTarget);    
        var $product = $target.parents("tr").find("input[name='product']");
        var $quantity = $target.parents("tr").find("input[name='quantity']");

        $product.each(function(){
            if(!$(this).val()){
                $(this).parents("tr").find("#s2id_product").addClass("error");
                product_empty = true;
            }else{
                $(this).parents("tr").find("#s2id_product").removeClass("error");
                product_empty = false;
            }
        });

        $quantity.each(function(){
            if(!$(this).val()){
                $(this).addClass("error");
                quantity_empty = true;
            }
            else{
                $(this).removeClass("error");
                quantity_empty = false;
            }
        });

        $target.parents("tr").find(".error").first().focus();

        if(!product_empty && !quantity_empty){
            $target.parents("tr").find("input[name='product']").each(function(){
                if ($(this).getAttributes()['id'] == 'product'){
                    $(this).attr("disabled", "disabled");
                }
            });
            $target.parents("tr").find("input[name='quantity']").each(function(){
                if ($(this).getAttributes()['id'] == 'quantity'){
                    $(this).attr("disabled", "disabled");
                }
            });

            $target.parents("tr").find(".add, .edit").toggle();
            $(".add-new").removeAttr("disabled");
        }
    },

    edit_row: function(e){
        e.preventDefault();
        e.stopPropagation();
        var $target = $(e.currentTarget);
        
        $target.parents("tr").find("select").each(function(){                
            if ($(this).getAttributes()['id'] == 'product'){
                $(this).removeAttr("disabled", "disabled");
            }
        });
        $target.parents("tr").find("input").each(function(){                
            if ($(this).getAttributes()['id'] == 'quantity'){
                $(this).removeAttr("disabled", "disabled");
            }
        });

        $target.parents("tr").find(".add, .edit").toggle();
        $(".add-new").attr("disabled", "disabled");
    },

    delete_row: function(e){
        e.preventDefault();
        e.stopPropagation();
        var $target = $(e.currentTarget);
        $target.parents("tr").remove();            
        $(".add-new").removeAttr("disabled");

        this.delete_row_number(e);
    },

    on_change_product: function(e){
        e.preventDefault();
        e.stopPropagation();            
        var $target = $(e.currentTarget);
        var $input = $target.parents("tr").find("input[name='product']");
        var $unit = $target.parents("tr").find("span[name='unit']");
        var unit = $input.select2('data');
    
        if(unit != null){                                              
            $unit[0].innerHTML  = unit.uom_id[1];
        }else{
            $unit[0].innerHTML  = '';
        }
    },

    on_change_quantity: function(e){
        e.preventDefault();
        e.stopPropagation();
        var $target = $(e.currentTarget);
        var quantity = $target.val();
        if (isNaN(quantity)){
            $target.val('');
        }
    },

    on_click_submit: function(e){
        e.preventDefault();
        e.stopPropagation();

        var self = this;
        
        var salesperson_empty = false;
        var product_empty = false;
        var quantity_empty = false;


        var $salesperson = $("input[name='salesperson']");

        if ($salesperson){
            if(!$salesperson.val()){
                $("#s2id_salesperson").addClass("error");
                salesperson_empty = true;
            } else{
                $("#s2id_salesperson").removeClass("error");
                salesperson_empty = false;
            }
        }

        var $table = $('.table_quick_quotation');
        var $product = $table.find("tr").find("input[name='product']");
        var $quantity = $table.find("tr").find("input[name='quantity']");

        $product.each(function(){
            if(!$(this).val()){
                $(this).parents("tr").find("#s2id_product").addClass("error");
                product_empty = true;
            }else{
                $(this).parents("tr").find("#s2id_product").removeClass("error");
                product_empty = false;
            }
        });

        $quantity.each(function(){
            if(!$(this).val()){
                $(this).addClass("error");
                quantity_empty = true;
            }
            else{
                $(this).removeClass("error");
                quantity_empty = false;
            }
        });

        if(!product_empty && !quantity_empty && !salesperson_empty){
            var data = [];

            $table.find("tbody tr").each(function(){
                var $input = $(this).find("input[name='product']");
                var product_id = $input.select2('data').id;
                
                var $quantity = $(this).find("input[name='quantity']");
                var qty = $quantity.val();
                
                var vals = {
                    'product_id': product_id,
                    'qty': qty,
                }
                data.push(vals);                    
            });
            
            var salesperson = $("input[name='salesperson']").val();

            if (data.length > 0){
                self.submit_quotation(data, salesperson);
            }
        }            
    },

    submit_quotation: function (data, salesperson) {            
        var self = this;
        return self.rpc('/portal_quick_quotation/submit_quick_quotation',{
                'data' : data,
                'salesperson': salesperson,
            }).then(function (res) {                
            var web_base_url = window.origin;
            if (res) {                    
                window.location = web_base_url + '/my/orders/' + res;
            } 
            else {
                self.displayNotification({ message: _t("Something went wrong during your new quotation.") });
            }
        })
    },

    on_search_prodcuts: function(e){
        e.preventDefault();
        var value = e.target.value.toLowerCase().trim();
        var $table = $('.table_quick_quotation');
        $table.find("tbody tr").each(function () {
            $(this).find("td:eq(1)").each(function () {
                var $input = $(this).find("input[name='product']");
                var text = $input.select2('data') ?  $input.select2('data').text : '';
                var id = text.toLowerCase().trim();
                var not_found = (id.indexOf(value) == -1);
                $(this).closest('tr').toggle(!not_found);
                return not_found;
            });
        });
    }
});

PublicWidget.registry.createNewQuotation = createNewQuotation;