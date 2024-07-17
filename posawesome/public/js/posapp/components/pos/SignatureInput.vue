<template>
    <v-dialog v-model="signatureDialog" max-width="500px">
        <v-card>
            <v-card-title class="headline">Enter Signature</v-card-title>
            <v-card-text>
                <div ref="signatureContainer" style="width: 100%; height: 200px; position: relative;">
                    <canvas ref="signatureCanvas" style="border: 1px solid #000;"></canvas>
                </div>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="error" @click="cancelSignature">Cancel</v-btn>
                <v-btn color="primary" @click="saveSignature">Save</v-btn>
                <v-btn color="caution" @click="clearSignature">Clear</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import SignaturePad from 'signature_pad';

export default {
    data() {
        return {
            signatureDialog: false,
            signaturePad: null,
        };
    },
    watch: {
        signatureDialog(val) {
            if (val) {
                this.$nextTick(() => {
                    requestAnimationFrame(() => {
                        this.initializeSignaturePad();
                    });                    
                });
            }
        },
    },
    methods: {
        openSignatureDialog() {
            this.signatureDialog = true;
        },
        initializeSignaturePad() {
            const canvas = this.$refs.signatureCanvas;
            // Adjust canvas size to fill the container
            canvas.width = this.$refs.signatureContainer.clientWidth;
            canvas.height = this.$refs.signatureContainer.clientHeight;

            // Initialize the signature pad with the new canvas element
            this.signaturePad = new SignaturePad(canvas, {
                penColor: '#000',
            });
        },
        saveSignature() {
            if (this.signaturePad.isEmpty()) {
               alert('Please provide a signature before saving.');
               return;
            }
            const signatureDataURL = this.signaturePad.toDataURL();
            // Emit the signature data back to the parent component (Proceed.vue)
            this.$emit('signature-entered', signatureDataURL);
            this.signatureDialog = false;
        },
        clearSignature() {
            if (this.signaturePad) {
                this.signaturePad.clear(); // Clear the signature pad data
            }            
        },
        cancelSignature() {
            this.signatureDialog = false;
        },
    },
};
</script>
