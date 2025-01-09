<!-- =============================================================== -->
<!-- ========================= Contact Section ===================== -->
<!-- =============================================================== -->

<h2 id="contact_section"> Contact Section </h2>
The <i>Contact Section</i> of the solver parameters input file is used to define the parameters controlling the contact computations
that prevents the geometric interpenetration of element domains.

A <i>Contact Section</i> is organized as follows 
<div style="background-color: #F0F0F0; padding: 10px; border: 1px solid #d0d0d0; border-left: 1px solid #d0d0d0">
&lt;<strong>Contact</strong> model=<i>contact_model</i>&gt; 
<br>
[ <a href="#contact_parameters"> Contact Parameters </a> ]
<br>
&lt;<strong>/Contact</strong>&gt;
</div>

The <strong>Contact</strong> keyword is used to define the parameters used in a contact computation. The <strong>model</strong> attribute 
<i>contact_model</i> is the name of a method used for the contact computation. The <strong>"penalty"</strong> model is currently the
only model supported.

<h3 id= "contact_parameters"> Contact Parameters </h3>
<div class="bc_param_div">
<strong>&lt;Closest_gap_to_activate_penalty></strong> <i>real</i> [1.0] <nobr>
<strong>&lt;/Closest_gap_to_activate_penalty&gt;</strong>
</nobr><br>
The maximum depth of penetration between elements in contact.
<br>
<strong>&lt;Desired_separation></strong> <i>real</i> [0.05] <nobr>
<strong>&lt;/Desired_separation&gt;</strong>
</nobr><br>
The minimum depth of penetration between elements in contact.
<br>
<strong>&lt;Min_norm_of_face_normals></strong> <i>real</i> [0.05] <nobr>
<strong>&lt;/Min_norm_of_face_normals&gt;</strong>
</nobr><br>
The minimum norm of face normals in contact.
<br>
<strong>&lt;Penalty_constant></strong> <i>real</i> [1e5] <nobr>
<strong>&lt;/Penalty_constant&gt;</strong>
</nobr><br>
The penalty constant used to prevent element interpenetration. 
<br>
</div>

