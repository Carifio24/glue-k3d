<template>
    <div class="glue-viewer-volume-3d">
        <div>
            <v-select label="reference" :items="reference_data_items" v-model="reference_data_selected" hide-details />
        </div>
        <div>
            <v-select label="x axis" :items="x_att_items" v-model="x_att_selected" hide-details />
        </div>
        <div>
            <v-select label="y axis" :items="y_att_items" v-model="y_att_selected" hide-details />
        </div>
        <div>
            <v-select label="z axis" :items="z_att_items" v-model="z_att_selected" hide-details />
        </div>
    </div>
</template>

<style id="viewer-k3d-volume">
    .glue-viewer-volume-3d .v-subheader.slider-label {
        font-size: 12px;
        height: 16px;
        margin-top: 6px;
    }
</style>
