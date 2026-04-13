// Profile Image Upload Handler
function profileImageUpload() {
    return {
        selectedFile: '',
        error: false,
        
        selectFile(event) {
            this.selectedFile = event.target.files[0]?.name || '';
            this.error = false;
        },
        
        validateSubmit(event) {
            if (!this.selectedFile) {
                event.preventDefault();
                this.error = true;
                setTimeout(() => this.error = false, 3000);
            }
        }
    }
}